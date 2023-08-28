from obj import Obj
import mathLib as ml
from mathLib import barycentricCoords
from math import pi,sin,cos,tan
from texture import Texture
from support import *

#Primitivas
POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3

class Model(object):
    def __init__(self,filename,translate=(0,0,0),rotate=(0,0,0),scale=(1,1,1)):
        model = Obj(filename)

        self.vertices = model.vertices
        self.textcoords = model.textcoords
        self.normals = model.normals
        self.faces = model.faces

        self.translate = translate
        self.rotate = rotate
        self.scale = scale

        self.texture = None
        self.normalMap = None

        self.SetShaders(None,None)

    def LoadTexture(self,textureName):
        self.texture = Texture(textureName)

    def LoadNormalMap(self, textureName):
        self.normalMap = Texture(textureName)

    def SetShaders(self,vertexShader,fragmentShader):
        self.vertexShader = vertexShader
        self.fragmentShader = fragmentShader

class Renderer(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.glClearColor(0,0,0)
        self.glClear()

        self.glColor(1,1,1)

        self.background = None

        self.objects = []

        self.vertexShader = None
        self.fragmentShader = None

        self.primitiveType = TRIANGLES

        self.activeTexture = None
        self.activeNormalMap = None

        self.activeModelMatrix = None

        self.glViewport(0,0,self.width,self.height)
        self.glCamMatrix()
        self.glProjectionMatrix()

        self.directionalLight = (1,0,0)

    def glBackgroundTexture(self,filename):
        self.background = Texture(filename)

    def glClearBackground(self):
        self.glClear()

        if self.background:
            # Para cada pixel del Viewport
            for x in range(self.vpX,self.vpX+self.vpWidth+1):
                for y in range(self.vpY, self.vpY + self.vpHeight + 1):

                    u=(x-self.vpX)/self.vpWidth
                    v=(y-self.vpY)/self.vpHeight

                    texColor = self.background.getColor(u,v)

                    if texColor:
                        self.glPoint(x,y,color(texColor[0],texColor[1],texColor[2]))

    def glPrimitiveAssembly(self,tVerts,uVerts,tTextCoords,tNormals):
        primitives = []
        if self.primitiveType==TRIANGLES:
            for i in range(0,len(tVerts),3):
                transformedVerts = []
                # Transformed Verts
                transformedVerts.append(tVerts[i])
                transformedVerts.append(tVerts[i + 1])
                transformedVerts.append(tVerts[i + 2])

                untransformedVerts = []
                # Untransformed Verts
                untransformedVerts.append(uVerts[i])
                untransformedVerts.append(uVerts[i + 1])
                untransformedVerts.append(uVerts[i + 2])

                # TextCoords
                texCoords = []
                texCoords.append(tTextCoords[i])
                texCoords.append(tTextCoords[i + 1])
                texCoords.append(tTextCoords[i + 2])

                # Normals
                normals = []
                normals.append(tNormals[i])
                normals.append(tNormals[i+1])
                normals.append(tNormals[i+2])

                triangle = [transformedVerts,untransformedVerts,texCoords,normals]

                primitives.append(triangle)

        return primitives

    def glClearColor(self,r,g,b):
        self.clearColor = color(r,g,b)

    def glColor(self,r,g,b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] for x in range(self.width)]
        self.zbuffer = [[float('inf') for y in range(self.height)] for x in range(self.width)]

    def glPoint(self,x,y,clr=None):
        if 0<=x<self.width and 0<=y<self.height:
            self.pixels[x][y] = clr or self.currColor

    def glTriangle(self,transformedVerts,untransformedVerts,texCoords,normals):
        A = transformedVerts[0]
        B = transformedVerts[1]
        C = transformedVerts[2]

        uA = untransformedVerts[0]
        uB = untransformedVerts[1]
        uC = untransformedVerts[2]

        minX = round(min(A[0],B[0],C[0]))
        maxX = round(max(A[0],B[0],C[0]))
        minY = round(min(A[1],B[1],C[1]))
        maxY = round(max(A[1],B[1],C[1]))

        tangent = None
        if self.activeNormalMap:
            edge1 = ml.subtract_arrays(uB, uA)
            edge2 = ml.subtract_arrays(uC, uA)

            deltaUV1 = ml.subtract_arrays(texCoords[1], texCoords[0])
            deltaUV2 = ml.subtract_arrays(texCoords[2], texCoords[0])

            try:
                f = 1 / (deltaUV1[0] * deltaUV2[1] - deltaUV2[0] * deltaUV1[1])
                tangent = [f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0]),
                           f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1]),
                           f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2])]

                tangent = ml.normalizar_vector(tangent)
            except:
                pass

        for x in range(minX,maxX+1):
            for y in range(minY,maxY+1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    P = (x,y)
                    bCoords=barycentricCoords(A,B,C,P)

                    if bCoords!=None:
                        u,v,w = bCoords

                        z = u*A[2]+v*B[2]+w*C[2]

                        if z<self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z

                            if self.fragmentShader != None:

                                colorP = self.fragmentShader(texture = self.activeTexture,
                                                             normalMap = self.activeNormalMap,
                                                             texCoords=texCoords,
                                                             normals=normals,
                                                             dLight = self.directionalLight,
                                                             bCoords=bCoords,
                                                             camMatrix=self.camMatrix,
                                                             modelMatrix=self.activeModelMatrix,
                                                             tangent=tangent)

                                self.glPoint(x, y, color(colorP[0],colorP[1],colorP[2]))
                            else:
                                self.glPoint(x, y, colorP)

    def glViewport(self,x,y,width,height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = int(width)
        self.vpHeight = int(height)
        self.vpMatrix = [[self.vpWidth/2,0,0,self.vpX+self.vpWidth/2],
                         [0,self.vpHeight/2,0,self.vpY+self.vpHeight/2],
                         [0,0,0.5,0.5],
                         [0,0,0,1]]

    def glCamMatrix(self,translate=(0,0,0),rotate=(0,0,0)):
        #Crea una matriz de camara
        self.camMatrix = self.glModelMatrix(translate,rotate)
        #La matriz de vista es igual a la inversa de la camara
        self.viewMatrix = ml.matriz_inversa(self.camMatrix)

    def glLookAt(self, camPos=(0, 0, 0), eyePos=(0, 0, 0)):
        worldUp = (0, 1, 0)
        forward = ml.subtract_arrays(camPos, eyePos)
        forward = ml.normalizar_vector(forward)

        rigth = ml.producto_cruz(worldUp, forward)
        rigth = ml.normalizar_vector(rigth)

        up = ml.producto_cruz(forward, rigth)
        up = ml.normalizar_vector(up)

        self.camMatrix = [[rigth[0], up[0], forward[0], camPos[0]],
                          [rigth[1], up[1], forward[1], camPos[1]],
                          [rigth[2], up[2], forward[2], camPos[2]],
                          [0, 0, 0, 1]]

        self.viewMatrix = ml.matriz_inversa(self.camMatrix)

    def glProjectionMatrix(self,fov=60,n=0.1,f=1000):
        aspectRatio = self.vpWidth/self.vpHeight
        t = tan((fov*pi/180)/2)*n
        r = t*aspectRatio

        self.projectionMatrix = [[n/r,0,0,0],
                                 [0,n/t,0,0],
                                 [0,0,-(f+n)/(f-n),-2*f*n/(f-n)],
                                 [0,0,-1,0]]

    def glModelMatrix(self,translate=(0,0,0),rotate=(0,0,0),scale=(1,1,1)):
        translation = [[1,0,0,translate[0]],
                       [0,1,0,translate[1]],
                       [0,0,1,translate[2]],
                       [0,0,0,1]]

        rotMat = self.glRotationMatrix(rotate[0],rotate[1],rotate[2])

        scaleMat = [[scale[0],0,0,0],
                    [0,scale[1],0,0],
                    [0,0,scale[2],0],
                    [0,0,0,1]]

        return ml.multiplicar_matrices(ml.multiplicar_matrices(translation,rotMat),scaleMat)

    def glRotationMatrix(self,pitch=0,yaw=0,roll=0):
        pitch += pi/180
        yaw *= pi/180
        roll *= pi/180

        pitchMat = [[1,0,0,0],
                    [0,cos(pitch),-sin(pitch),0],
                    [0,sin(pitch),cos(pitch),0],
                    [0,0,0,1]]

        yawMat = [[cos(yaw),0,sin(yaw),0],
                  [0,1,0,0],
                  [-sin(yaw),0,cos(yaw),0],
                  [0,0,0,1]]

        rollMat = [[cos(roll),-sin(roll),0,0],
                   [sin(roll),cos(roll),0,0],
                   [0,0,1,0],
                   [0,0,0,1]]

        return ml.multiplicar_matrices(ml.multiplicar_matrices(pitchMat,yawMat),rollMat)

    def glAddModel(self,model):
        self.objects.append(model)

    def glRender(self):

        for model in self.objects:
            transformedVerts = []
            untransformedVerts = []
            textCoords = []
            normals = []

            self.vertexShader = model.vertexShader
            self.fragmentShader = model.fragmentShader
            self.activeTexture = model.texture
            self.activeNormalMap = model.normalMap
            self.activeModelMatrix = self.glModelMatrix(model.translate,model.rotate,model.scale)

            for face in model.faces:
                vertCount = len(face)
                v0 = model.vertices[face[0][0]-1]
                v1 = model.vertices[face[1][0]-1]
                v2 = model.vertices[face[2][0]-1]
                if vertCount == 4:
                    v3 = model.vertices[face[3][0]-1]

                untransformedVerts.append(v0)
                untransformedVerts.append(v1)
                untransformedVerts.append(v2)
                if vertCount == 4:
                    untransformedVerts.append(v0)
                    untransformedVerts.append(v2)
                    untransformedVerts.append(v3)

                vt0 = model.textcoords[face[0][1] - 1]
                vt1 = model.textcoords[face[1][1] - 1]
                vt2 = model.textcoords[face[2][1] - 1]
                if vertCount == 4:
                    vt3 = model.textcoords[face[3][1] - 1]

                vn0 = model.normals[face[0][2] - 1]
                vn1 = model.normals[face[1][2] - 1]
                vn2 = model.normals[face[2][2] - 1]
                if vertCount == 4:
                    vn3 = model.normals[face[3][2] - 1]

                if self.vertexShader:
                    v0 = self.vertexShader(v0,modelMatrix=self.activeModelMatrix,viewMatrix=self.viewMatrix,projectionMatrix=self.projectionMatrix,vpMatrix=self.vpMatrix,normal=vn0)
                    v1 = self.vertexShader(v1, modelMatrix=self.activeModelMatrix,viewMatrix=self.viewMatrix,projectionMatrix=self.projectionMatrix,vpMatrix=self.vpMatrix,normal=vn1)
                    v2 = self.vertexShader(v2, modelMatrix=self.activeModelMatrix,viewMatrix=self.viewMatrix,projectionMatrix=self.projectionMatrix,vpMatrix=self.vpMatrix,normal=vn2)

                    if vertCount == 4:
                        v3 = self.vertexShader(v3, modelMatrix=self.activeModelMatrix,viewMatrix=self.viewMatrix,projectionMatrix=self.projectionMatrix,vpMatrix=self.vpMatrix,normal=vn3)

                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)
                if vertCount==4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)


                textCoords.append(vt0)
                textCoords.append(vt1)
                textCoords.append(vt2)
                if vertCount==4:
                    textCoords.append(vt0)
                    textCoords.append(vt2)
                    textCoords.append(vt3)

                normals.append(vn0)
                normals.append(vn1)
                normals.append(vn2)
                if vertCount == 4:
                    normals.append(vn0)
                    normals.append(vn2)
                    normals.append(vn3)

            primitives = self.glPrimitiveAssembly(transformedVerts,untransformedVerts,textCoords,normals)

            # Rasterizando las primitivas
            for prim in primitives:
                if self.primitiveType==TRIANGLES:
                    self.glTriangle(prim[0],prim[1],prim[2],prim[3])

    def glFinish(self,filename):
        with open(filename,"wb") as file:
            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14+40+(self.width*self.height*3)))
            file.write(dword(0))
            file.write(dword(14+40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword((self.width*self.height*3)))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
