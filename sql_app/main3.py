from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

html = """
<!doctype html> 
<html lang="en"> 
<head> 
  <meta charset="utf-8"> 
  <meta name="viewport" content="width=device-width, initial-scale=1"> 
  <title>Autocomplete using Jquery</title> 
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui. 
css"> 
  <link rel="stylesheet" href="/resources/demos/style.css"> 
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script> 
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script> 
  <script> 
  $( function() { 
    var tags = [ "dabeli" , "vadapau", "paneer" , "papad",
                  "buttermilk" , "roti" , "dal- rice" , "idali" , "upama",
                  "dosa"  
    ]; 
    $( "#tags" ).autocomplete({ 
      source: tags 
  
/* #tthe ags is the id of the input element 
source: tags is the list of available tags*/ 
  
  
    }); 
  } ); 
  </script> 
</head> 
<body> 
   
<div class="ui-widget"> 
 <H3>Enter an alphabet to get suggestion:</H3> 
  <input id="tags"> 
</div> 
   
</body> 
</html> 

"""


@app.get("/")
async def get():
    return HTMLResponse(html)


if __name__ == "__main__":
    uvicorn.run("main3:app")

