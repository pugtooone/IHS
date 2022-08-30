#target photoshop;

app.bringToFront();
function main(){
    hideLayers(activeDocument);
}


function hideLayers(ref){
    var len = ref.layers.length;

    for(var i = 0 ; i < len ; i++){
        if(ref.layers[i].kind == 'LayerKind.SOLIDFILL'){
            ref.layers[i].visible = false;
            for (var j = i ; j < len  ; j++){
                ref.layers[j].visible = false;
            }

        }
    }

}


main();