#target photoshop;

app.bringToFront();
function main(){
    hideLayers(activeDocument);
}


function hideLayers(ref){
    var len = ref.layers.length;

    for(var i = 0 ; i < len ; i++){
        if(ref.layers[i].kind == 'LayerKind.SOLIDFILL'){
            ref.activeLayer = ref.layers[i];
            ref.layers[i].visible = false;
            var desc5 = new ActionDescriptor();

            var ref1 = new ActionReference();
        
            var idcontentLayer = stringIDToTypeID( "contentLayer" );
        
            ref1.putClass( idcontentLayer );
        
            desc5.putReference( charIDToTypeID( "null" ), ref1 );
        
            var desc6 = new ActionDescriptor();
        
                var desc7 = new ActionDescriptor();
        
                    var desc8 = new ActionDescriptor();
        
                    desc8.putDouble( charIDToTypeID( "Rd  " ), 255.000000 );
        
                    desc8.putDouble( charIDToTypeID( "Grn " ), 255.000000 );
        
                    desc8.putDouble( charIDToTypeID( "Bl  " ), 255.000000 );
        
                desc7.putObject( charIDToTypeID( "Clr " ), charIDToTypeID( "RGBC" ), desc8 );
        
            desc6.putObject( charIDToTypeID( "Type" ), stringIDToTypeID( "solidColorLayer" ), desc7 );
        
        desc5.putObject( charIDToTypeID( "Usng" ), idcontentLayer, desc6 );
        
        executeAction( charIDToTypeID( "Mk  " ), desc5, DialogModes.NO );

        return;
        }
    }

}


main();