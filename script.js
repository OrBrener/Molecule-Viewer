/* javascript to accompany jquery.html */

$(document).ready( 
    /* this defines a function that gets called after the document is in memory */
    function()
    {
        $("#uploadSDF").click(
            function()
            {
            //     location.href = "/uploadSDF";
            const form = new FormData()
            
            const file = $("#SDFFileInput")[0].files[0]
            const name = $("#MoleculeNameInput").val()

            form.append("file", file)
            form.append("name", name)
        
            $.ajax( {
                url: 'uploadSDF',
                type: 'POST',
                data: form,
                contentType: false,
                processData: false,

                success: function() {
                    alert("Success!!!");
                    location.href = 'http://localhost:50102/uploadSDF.html'
                },
                error: function() {
                    alert("Failure");
                 }
                } );
            }
            
        )
        if($('#heading0').length){
            $('#hidden').css('display', 'none');
        }
    } );
  