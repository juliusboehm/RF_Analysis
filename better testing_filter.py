import pandas as pd

#Track 0 = Robo
#Track 1 = Finch

input = pd.read_csv("8436_aktiv.000_8436_aktiv_snip.analysis (1).csv")
input.to_csv("better_filter_copy.csv", index=False)
input = pd.read_csv("better_filter_copy.csv")

col = ["FrameID", "Head_x", "Head_y", "Beak_x", "Beak_y", "Robot_x", "Robot_y", "Robot_visible"]

output = pd.DataFrame(columns=col, index=range(len(input)-1))

for i in range(len(input)-1):
    line_A = input.loc[i]
    line_B = input.loc[i+1]

    if line_A["track"] == "track_1" and line_B["track"] == "track_0":           #Finch + Robo -> nothing must happen
        pass

    elif line_A["track"] == "track_0" and line_B["track"] == "track_1":         #Robo + Finch
        output.loc[i]["FrameID"] = line_B["frame_idx"]      #Frame
        output.loc[i]["Head_x"] = line_B["head_finch.x"]    #Head_x
        output.loc[i]["Head_y"] = line_B["head_finch.y"]    #Head_y
        output.loc[i]["Beak_x"] = line_B["beak_finch.x"]    #Beak_x
        output.loc[i]["Beak_y"] = line_B["beak_finch.y"]    #Beak_y
        output.loc[i]["Robot_x"] = line_A["head_finch.x"]   #Robot_x
        output.loc[i]["Robot_y"] = line_A["head_finch.x"]   #Robot_y
        output.loc[i]["Robot_visible"] = 0                  #Robot_visible default
    
    elif line_A["track"] == "track_1" and line_B["track"] == "track_1":         #Finch + Finch -> Robo missing
        output.loc[i]["FrameID"] = line_B["frame_idx"]      #Frame
        output.loc[i]["Head_x"] = line_B["head_finch.x"]    #Head_x
        output.loc[i]["Head_y"] = line_B["head_finch.y"]    #Head_y
        output.loc[i]["Beak_x"] = line_B["beak_finch.x"]    #Beak_x
        output.loc[i]["Beak_y"] = line_B["beak_finch.y"]    #Beak_y
        output.loc[i]["Robot_x"] = 0                        #Robot_x
        output.loc[i]["Robot_y"] = 0                        #Robot_y
        output.loc[i]["Robot_visible"] = 0                  #Robot_visible default
    
    #elif line_A["track"] == "track_0" and line_B["track"] == "track_0":         #Robo + Robo -> Finch missing
    #    output.loc[i]["FrameID"] = line_B["frame_idx"]      #Frame
    #    output.loc[i]["Head_x"] = 0                         #Head_x
    #    output.loc[i]["Head_y"] = 0                         #Head_y
    #    output.loc[i]["Beak_x"] = 0                         #Beak_x
    #    output.loc[i]["Beak_y"] = 0                         #Beak_y
    #    output.loc[i]["Robot_x"] = line_A["head_finch.x"]   #Robot_x
    #    output.loc[i]["Robot_y"] = line_A["head_finch.x"]   #Robot_y
    #    output.loc[i]["Robot_visible"] = 0                  #Robot_visible default

    else:
        pass

output = output.dropna()    #drop NANs

output.to_csv('endproduct.csv', index=False)
print("---EXECUTED---")