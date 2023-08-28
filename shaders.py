import mathLib as ml
import random

def vertexShader(vertex,**kwargs):

    #El vertex shader se lleva a cabo por cada vertices
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    vpMatrix = kwargs["vpMatrix"]

    vt = [vertex[0],vertex[1],vertex[2],1]

    vt = ml.multiplicar_matriz_vector(ml.multiplicar_matrices(ml.multiplicar_matrices(ml.multiplicar_matrices(vpMatrix,projectionMatrix),viewMatrix),modelMatrix),vt)
    vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]
    return vt

def gouradShader(**kwargs):
    texture = kwargs["texture"]
    tA,tB,tC = kwargs["texCoords"]
    nA,nB,nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u,v,w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture !=None:
        tU = u*tA[0]+v*tB[0]+w*tC[0]
        tV = u*tA[1]+v*tB[1]+w*tC[1]

        textureColor = texture.getColor(tU,tV)
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]

    normal = [u*nA[0]+v*nB[0]+w*nC[0],
              u*nA[1]+v*nB[1]+w*nC[1],
              u*nA[2]+v*nB[2]+w*nC[2],
              0]

    normal = ml.multiplicar_matriz_vector(modelMatrix,normal)
    normal = [normal[0],normal[1],normal[2]]

    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] *= -1
    intensity = ml.producto_punto(normal, dLight)

    b *= intensity
    g *= intensity
    r *= intensity

    if b >= 1.0:
        b = 1.0
    if g >= 1.0:
        g = 1.0
    if r >= 1.0:
        r = 1.0

    if intensity > 0:
        return r, g, b
    else:
        return (0, 0, 0)

def toonShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture != None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]

        textureColor = texture.getColor(tU, tV)
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2],
              0]

    normal = ml.multiplicar_matriz_vector(modelMatrix, normal)
    normal = [normal[0], normal[1], normal[2]]

    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] *= -1
    intensity = ml.producto_punto(normal, dLight)

    if intensity <= 0.25:
        intensity = 0.2
    elif intensity<= 0.5:
        intensity = 0.45
    elif intensity<= 0.75:
        intensity = 0.7
    elif intensity<=1:
        intensity = 0.95

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return (0, 0, 0)

def normalMapShader(**kwargs):
    texture = kwargs["texture"]
    normalMap = kwargs["normalMap"]
    tA,tB,tC = kwargs["texCoords"]
    nA,nB,nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u,v,w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]
    tangent = kwargs["tangent"]

    b = 1.0
    g = 1.0
    r = 1.0
    tU = u * tA[0] + v * tB[0] + w * tC[0]
    tV = u * tA[1] + v * tB[1] + w * tC[1]
    if texture !=None:

        textureColor = texture.getColor(tU,tV)
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]

    normal = [u*nA[0]+v*nB[0]+w*nC[0],
              u*nA[1]+v*nB[1]+w*nC[1],
              u*nA[2]+v*nB[2]+w*nC[2],
              0]

    normal = ml.multiplicar_matriz_vector(modelMatrix,normal)
    #normal = normal.toList()[0]
    normal = [normal[0],normal[1],normal[2]]
    normal = ml.normalizar_vector(normal)


    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] *= -1

    if normalMap:
        texNormal = normalMap.getColor(tU,tV)
        texNormal = [texNormal[0]*2-1,
                     texNormal[1]*2-1,
                     texNormal[2]*2-1]
        texNormal = ml.normalizar_vector(texNormal)

        bitangent = ml.producto_cruz(normal,tangent)
        bitangent = ml.normalizar_vector(bitangent)

        tangent = ml.producto_cruz(normal,bitangent)
        tangent = ml.normalizar_vector(tangent)

        tangenMatrix = [[tangent[0],tangent[1],tangent[2]],
                        [bitangent[0],bitangent[1],bitangent[2]],
                        [normal[0],normal[1],normal[2]]]
        texNormal = ml.multiplicar_matriz_vector(tangenMatrix,texNormal)
        #texNormal = texNormal.toList()[0]
        texNormal = ml.normalizar_vector(texNormal)
        intensity = ml.producto_punto(texNormal,dLight)
    else:
        intensity = ml.producto_punto(normal, dLight)

    b *= intensity
    g *= intensity
    r *= intensity

    if b>=1.0:
        b=1.0
    if g>=1.0:
        g=1.0
    if r>=1.0:
        r=1.0

    if intensity > 0:
        return r, g, b
    else:
        return (0, 0, 0)

def negativeShader(**kwargs):
    texture = kwargs["texture"]
    tA,tB,tC = kwargs["texCoords"]
    u,v,w = kwargs["bCoords"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture !=None:
        tU = u*tA[0]+v*tB[0]+w*tC[0]
        tV = u*tA[1]+v*tB[1]+w*tC[1]

        textureColor = texture.getColor(tU,tV)
        b*=1-textureColor[2]
        g*=1-textureColor[1]
        r*=1-textureColor[0]
        return r, g, b
    else:
        return (0, 0, 0)

def layerShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture != None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]

        textureColor = texture.getColor(tU, tV)
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2],
              0]

    normal = ml.multiplicar_matriz_vector(modelMatrix, normal)
    normal = [normal[0], normal[1], normal[2]]

    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] *= -1
    intensity = ml.producto_punto(normal, dLight)

    color = (1,1,1)
    if intensity <= 0.25:
        color = (1, 0, 0)
    elif intensity <= 0.4:
        color = (1, 1, 0)
    elif intensity <= 0.6:
        color = (1, 0, 1)
    elif intensity <= 0.8:
        color = (0, 1, 0)
    elif intensity <= 1:
        color = (0, 0, 1)

    b += intensity * color[2]
    g += intensity * color[1]
    r += intensity * color[0]

    if b >= 1.0:
        b = 1.0
    if g >= 1.0:
        g = 1.0
    if r >= 1.0:
        r = 1.0

    if intensity>0:
        return r, g, b
    else:
        return (0,0,0)

def blackAndWhiteShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]

    if texture is not None:
        tU = tA[0] + tB[0] + tC[0]
        tV = tA[1] + tB[1] + tC[1]

        textureColor = texture.getColor(tU/3, tV/3)
        gray_value = (textureColor[0] + textureColor[1] + textureColor[2]) / 3

        return gray_value, gray_value, gray_value
    else:
        return (1.0, 1.0, 1.0)

def staticShader(**kwargs):
    return (random.random(),random.random(),random.random())




