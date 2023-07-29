import osascript
target_volume = 50
vol = "set volume output volume " + str(50)
osascript.osascript(vol)

# or
target_volume = 50
osascript.osascript("set volume output volume {}".format(target_volume))

# or
osascript.osascript("set volume output volume 50")
(0, 'output volume:50, input volume:58, alert volume:100, output muted:false', '')
result = osascript.osascript('get volume settings')
print(result)
print(type(result))
volInfo = result[1].split(',')
outputVol = volInfo[0].replace('output volume:', '')
print(outputVol)
