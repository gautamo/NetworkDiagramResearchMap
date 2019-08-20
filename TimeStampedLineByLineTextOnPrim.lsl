key requestURL;

//Example Script using a function to set text on a prim, line by line

//gets the last index of the specified character in a string
integer uSubStringLastIndex( string vStrSrc, string vStrTst ){
    integer vIdxFnd =
      llStringLength( vStrSrc ) -
      llStringLength( vStrTst ) -
      llStringLength(
        llList2String(
          llParseStringKeepNulls( vStrSrc, (list)vStrTst, [] ),
          0xFFFFFFFF ) //-- (-1)
        );
    return (vIdxFnd | (vIdxFnd >> 31));
}

//Texture settings may need to be adjusted to fit the texture
display_text_on_prim(string text){
    
    //change these values to suit your needs
    integer fontSize = 6;
    string fontName = "Arial";
    integer lineSpacing = 12;
    integer charPerLine = 72;
    
    //start of first letter
    integer x = 10;
    integer y = 10;

    integer textlen = llStringLength(text);
    //llOwnerSay("TEXT LENGTH: " + textlen);
    //llOwnerSay("Full text: " + text);

    integer start = 0;
    integer end = charPerLine;
    integer stop = 0;
    
    string CommandList = "";
    CommandList = osSetFontSize( CommandList, fontSize); 
    CommandList = osSetFontName( CommandList, fontName);
    
    while (stop == 0){
         //llOwnerSay("pre start/end: " + start + "/" + end);
         
        if (textlen < charPerLine){
            end = textlen;   
        }
        else if (end != textlen){
            string tempsubtext = llGetSubString(text, 0, end);
           
            integer lastSpace = uSubStringLastIndex(tempsubtext, " ");
           
            end = lastSpace;
            //llOwnerSay("Last Space: " + lastSpace);
         }
        
         
         
         
         string subtext = llGetSubString(text, start, end);
         
         //llOwnerSay("post start/end: " + start + "/" + end);
         //llOwnerSay("Subtext: " + subtext);
         //llOwnerSay("x y: " + x + " " + y);
         
         CommandList = osMovePen( CommandList, x, y);
         CommandList = osDrawText( CommandList, subtext);
         osSetDynamicTextureData( "", "vector", CommandList, "width:256,height:256", 0);
         
         start = end+1;
         y += lineSpacing;
         
         if (end+charPerLine > textlen){
             end = textlen;
             }
         else{
             end+=charPerLine;
            }
        
         if (start >= textlen){
             stop = 1;
             //llOwnerSay("FOUND END");
             break;
            }
    }
    //llOwnerSay("script ended");
    
    //Add timestamp (format is YYYY-MM-DDThh:mm:ss.ff..fZ)
    list TimeStamp = llParseString2List(llGetTimestamp(),["-",":"],["T"]); //Get timestamp and split into parts in a list
    string hour = llList2String(TimeStamp,4);
    string minute = llList2String(TimeStamp,5);
    string second = llList2String(TimeStamp,6);
    string day = llList2String(TimeStamp,2);
    string month = llList2String(TimeStamp,1);
    string year = llList2String(TimeStamp,0);
    
    string timestamp = "Last Updated: " + month + " / " + day + " / " + year + " at " + hour + ":" + minute + " UTC";

    CommandList += "PenColour Red;";
    CommandList = osMovePen( CommandList, x, y);
    CommandList = osDrawText( CommandList, timestamp);
    osSetDynamicTextureData( "", "vector", CommandList, "width:256,height:256", 0);
    
}

default
{
    state_entry()
    {
        requestURL = llRequestURL();     // Request that an URL be assigned to me.
        //string thisText = "Trial 3: Let's display a text summary";
        //display_text_on_prim(thisText);      
    }
     http_request(key id, string method, string body) 
     {
        if ((method == URL_REQUEST_GRANTED) && (id == requestURL) )
        {
            // An URL has been assigned to me.
            llOwnerSay("Obtained URL: " + body);
            requestURL = NULL_KEY;
        }
        else if ((method == URL_REQUEST_DENIED) && (id == requestURL)) 
        {
            // I could not obtain a URL
            llOwnerSay("There was a problem, and an URL was not assigned: " + body);
            requestURL = NULL_KEY;
        }

        else if (method == "POST") 
        {
            // An incoming message was received.
            llOwnerSay("Received information from the outside: " + body);
            llHTTPResponse(id,200,"Message received.");
        
            display_text_on_prim(body);  
        }
        else 
        {
            // An incoming message has come in using a method that has not been anticipated.
            llHTTPResponse(id,405,"Unsupported Method");
        }
    }
    
    
    
}