import shaders
from gl import Renderer, Model

width = 1920
height = 1080

rend = Renderer(width,height)

rend.glClearColor(0.2,0.2,0.2)
rend.glClear()

rend.glBackgroundTexture("backgrounds/space.bmp")
rend.glClearBackground()

rend.directionalLight = (0,0,-1)

model = Model(filename="models/planet.obj",translate=(3,1.7,-5),rotate=(0,-45,0),scale=(1,1,1))
model.LoadTexture("textures/earth.bmp")
model.LoadNormalMap("textures/earth_normalmap.bmp")
model.SetShaders(shaders.vertexShader,shaders.normalMapShader)

model2 = Model(filename="models/toonRocket.obj",translate=(2.5,-1,-6),rotate=(0,-45,0),scale=(1,1,1))
model2.LoadTexture("textures/toonRocket.bmp")
model2.SetShaders(shaders.vertexShader,shaders.toonShader)

model3 = Model(filename="models/alien.obj",translate=(-3.8,0.55,-5),rotate=(0,-25,0),scale=(0.6,0.6,0.6))
model3.LoadTexture("textures/alien.bmp")
model3.SetShaders(shaders.vertexShader,shaders.layerShader)
model3_2 = Model(filename="models/alien.obj",translate=(-3.5,0.55,-5),rotate=(0,-25,0),scale=(0.4,0.4,0.4))
model3_2.LoadTexture("textures/alien.bmp")
model3_2.SetShaders(shaders.vertexShader,shaders.staticShader)

model4 = Model(filename="models/planet.obj",translate=(-3,-2,-5),rotate=(0,0,0),scale=(2.7,2.7,2.7))
model4.LoadTexture("textures/moon.bmp")
model4.SetShaders(shaders.vertexShader,shaders.gouradShader)

model5 = Model(filename="models/satelite.obj",translate=(-3,3,-8),rotate=(0,45,45),scale=(0.7,0.7,0.7))
model5.LoadTexture("textures/satelite.bmp")
model5.SetShaders(shaders.vertexShader,shaders.blackAndWhiteShader)

model6 = Model(filename="models/saturn.obj",translate=(6,-3,-8),rotate=(0,45,0),scale=(0.5,0.5,0.5))
model6.LoadTexture("textures/saturn.bmp")
model6.SetShaders(shaders.vertexShader,shaders.negativeShader)

rend.glAddModel(model)
rend.glAddModel(model2)
rend.glAddModel(model3)
rend.glAddModel(model3_2)
rend.glAddModel(model4)
rend.glAddModel(model5)
rend.glAddModel(model6)

rend.glRender()

rend.glFinish("output.bmp")