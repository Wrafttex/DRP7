def esptableLayout(roomjson):
    tableclass ="table table-hover"
    thscope = "<th scope=\"col\">"
    startlayout = f" <table class=\"{tableclass}\"> <thead> <tr> {thscope}ESP Name</th> {thscope}Occupancy detection</th></tr></thead><tbody>"
    
    for index in range(len(roomjson["RoomOccupancy"])):
        roomid = str(roomjson['RoomOccupancy'][index]['ESPId']).split("/")[-1]
        buttonlayout = f"<tr><th scope=\"row\"><button type=\"button\" data-toggle=\"modal\" data-target=\"#Modal{roomid}\" class=\"btn btn-light\">{roomid}</button>"
        occuchecker = roomjson['RoomOccupancy'][index]["Occupants"]>0
        occulayout = f"</th><td>{occuchecker!s}</td></tr>"
        startlayout = f"{startlayout} {buttonlayout} {occulayout}"
    startlayout = f"{startlayout}  </tbody> </table>"
    for index in range(len(roomjson["RoomOccupancy"])):
        roomid = str(roomjson['RoomOccupancy'][index]['ESPId']).split("/")[-1]
        startmodallayout = f"<div class=\"modal fade\" id=\"Modal{roomid}\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"Modal{roomid}Title\" aria-hidden=\"true\">"    
        headmodallayout = f"<div class=\"modal-dialog modal-dialog-centered\" role=\"document\"> <div class=\"modal-content\"> <div class=\"modal-header\"> <h5 class=\"modal-title\" id=\"Modal{roomid}Title\">{roomid}</h5> <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>"
        bodymodalstarterlayout = f"<div class=\"modal-body\"><table class=\"table\"><thead><tr><th scope=\"col\">param</th><th scope=\"col\">Value</th></tr></thead><tbody>"
        
        for contentkey in roomjson["RoomOccupancy"][index].keys():
            bodymodalcontentlayout = f"<tr><th scope=\"row\">{contentkey}</th><td>{roomjson['RoomOccupancy'][index][contentkey]}</td></tr><tr>"
            bodymodalstarterlayout = f"{bodymodalstarterlayout} {bodymodalcontentlayout}"
        footermodallayout = f"</tbody></table></div><div class=\"modal-footer\"></div></div></div></div>"
        startlayout = f"{startlayout} {startmodallayout} {headmodallayout} {bodymodalstarterlayout} {footermodallayout}"
    
    return startlayout   

def espdivLayout(roomjson):
    divscope = "<div class=\"row\">"
    outerdivclass ="col-6 col-sm-6 col-md-4 col-lg-2 col-xl-1"
    innerdivclass = "border border-dark mx-auto my-1 row"
    
    
    startlayout = f" <div class=\"container-fluid\"> {divscope} "
    for index in range(len(roomjson["RoomOccupancy"])):
        roomid = str(roomjson['RoomOccupancy'][index]['ESPId']).split("/")[-1]
        colorcondition = "green" if roomjson['RoomOccupancy'][index]["Occupants"] > 0 else "red"
        
        dotclass = f'style=\"height: 35px; width: 35px!important; background-color: {colorcondition}; border-radius:50%; display:inline-block;text-align:right;\"'
        outerdiv = f"<div class=\"{outerdivclass}\">"
        innerdiv = f"<div class=\"{innerdivclass}\"><h5 class=\"col pl-0 mt-1 ml-1\"><button type=\"button\" data-toggle=\"modal\" data-target=\"#Modal{roomid}\" class=\"btn btn-secondary\">{roomid}</button> </h5> <span class=\"col-auto ml-auto mr-1 mb-1\" {dotclass}></span></div></div>"
        # buttonlayout = f"<tr><th scope=\"row\"><button type=\"button\" data-toggle=\"modal\" data-target=\"#Modal{roomjson['RoomOccupancy'][index]['ESPId']}\" class=\"btn btn-light\">{roomjson['RoomOccupancy'][index]['ESPId']}</button>"
        # occuchecker = roomjson['RoomOccupancy'][index]["Occupants"]>0
        # occulayout = f"</th><td>{occuchecker!s}</td></tr>"
        startlayout = f"{startlayout} {outerdiv} {innerdiv}"
    startlayout = f"{startlayout}  </div> </div>"
    for index in range(len(roomjson["RoomOccupancy"])):
        roomid = str(roomjson['RoomOccupancy'][index]['ESPId']).split("/")[-1]
        startmodallayout = f"<div class=\"modal fade\" id=\"Modal{roomid}\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"Modal{roomid}Title\" aria-hidden=\"true\">"    
        headmodallayout = f"<div class=\"modal-dialog modal-dialog-centered\" role=\"document\"> <div class=\"modal-content\"> <div class=\"modal-header\"> <h5 class=\"modal-title\" id=\"Modal{roomjson['RoomOccupancy'][index]['ESPId']}Title\">{roomjson['RoomOccupancy'][index]['ESPId']}</h5> <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>"
        bodymodalstarterlayout = f"<div class=\"modal-body\"><table class=\"table\"><thead><tr><th scope=\"col\">param</th><th scope=\"col\">Value</th></tr></thead><tbody>"
        
        for contentkey in roomjson["RoomOccupancy"][index].keys():
            bodymodalcontentlayout = f"<tr><th scope=\"row\">{contentkey}</th><td>{roomjson['RoomOccupancy'][index][contentkey]}</td></tr><tr>"
            bodymodalstarterlayout = f"{bodymodalstarterlayout} {bodymodalcontentlayout}"
        footermodallayout = f"</tbody></table></div><div class=\"modal-footer\"></div></div></div></div>"
        startlayout = f"{startlayout} {startmodallayout} {headmodallayout} {bodymodalstarterlayout} {footermodallayout}"
    
    return startlayout   