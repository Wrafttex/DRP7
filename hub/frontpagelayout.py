def espGridLayout(roomjson):
    print(roomjson)
    divscope = "<div class=\"row\">"
    outerdivclass ="col-6 col-sm-6 col-md-4 col-lg-2 col-xl-1"
    innerdivclass = "border border-dark mx-auto my-1 row"
    header5class = "col pl-0 mt-1 ml-1"
    secbtnclass = "btn btn-secondary"
    dangerbtnclass= "btn btn-danger "
    startlayout = f" <div class=\"container-fluid\"> {divscope} "
    circleclass = "col-auto ml-auto mr-1 mb-1"
    outerdiv = f"<div class=\"{outerdivclass}\">"
    dotstyle = "height: 35px; width: 35px!important; border-radius:50%; display:inline-block;text-align:right; "
    headmodallclass = "modal-dialog modal-dialog-centered"
    innerdiv = f"<div class=\"{innerdivclass}\"><h5 class=\"{header5class}\">"
    try:
        for index in range(len(roomjson["RoomOccupancy"])):
            roomid = str(roomjson['RoomOccupancy'][index]['ESPId']).split("/")[-1]
            colorcondition = "green" if roomjson['RoomOccupancy'][index]["Occupants"] > 0 else "red"
            print(roomjson['RoomOccupancy'][index]["Occupants"])
            dotclass = f'style=\"background-color: {colorcondition}; {dotstyle} \"'
            
            innercontentdiv = f"<button type=\"button\" data-toggle=\"modal\" data-target=\"#Modal{roomid}\" class=\"{secbtnclass}\">{roomid}</button> </h5> <span class=\"{circleclass}\" {dotclass}>"
            startlayout = f"{startlayout} {outerdiv} {innerdiv} {innercontentdiv} </span></div></div>"
        startlayout = f"{startlayout}  </div> </div>"
        for index in range(len(roomjson["RoomOccupancy"])):
            roomid = str(roomjson['RoomOccupancy'][index]['ESPId']).split("/")[-1]
            fullid = roomjson['RoomOccupancy'][index]['ESPId']
            startmodallayout = f"<div class=\"modal fade\" id=\"Modal{roomid}\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"Modal{roomid}Title\" aria-hidden=\"true\">"    
            headmodallayout = f"<div class=\"{headmodallclass}\" role=\"document\"> <div class=\"modal-content\"> <div class=\"modal-header\"> <h5 class=\"modal-title\" id=\"Modal{fullid}Title\">{fullid}</h5> <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>"
            bodymodalstarterlayout = f"<div class=\"modal-body\"><table class=\"table\"><thead><tr><th scope=\"col\">param</th><th scope=\"col\">Value</th></tr></thead><tbody>"
            
            for contentkey in roomjson["RoomOccupancy"][index].keys():
                bodymodalcontentlayout = f"<tr><th scope=\"row\">{contentkey}</th><td>{roomjson['RoomOccupancy'][index][contentkey]}</td></tr><tr>"
                bodymodalstarterlayout = f"{bodymodalstarterlayout} {bodymodalcontentlayout}"
                
            footermodallayout = f"</tbody></table><button class=\"{dangerbtnclass}\" id=\"deletebtn_{fullid}\" type=\"button\">Delete</button><h2 id=\"status_{roomid}\"></h2></div><div class=\"modal-footer\"></div></div></div></div>"
            startlayout = f"{startlayout} {startmodallayout} {headmodallayout} {bodymodalstarterlayout} {footermodallayout}"
    except TypeError:
        startlayout=""
    
    return startlayout   
