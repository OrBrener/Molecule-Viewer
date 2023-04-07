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

        $("#elementSubmit").click(
            function()
            {
            const form = new FormData()
            
            const num = $("#inputElementNumber").val()
            const code = $("#inputElementCode").val()
            const name = $("#inputElementName").val()
            const col1 = $("#inputColor1").val()
            const col2 = $("#inputColor2").val()
            const col3 = $("#inputColor3").val()
            const radius = $("#inputRadius").val()

            form.append("num", num)
            form.append("code", code)
            form.append("name", name)
            form.append("col1", col1)
            form.append("col2", col2)
            form.append("col3", col3)
            form.append("radius", radius)
        
            $.ajax( {
                url: 'elementSubmit',
                type: 'POST',
                data: form,
                contentType: false,
                processData: false,

                success: function() {
                    alert("Success!!!");
                    location.href = 'http://localhost:50102/addElements.html'
                },
                error: function() {
                    alert("Failure");
                 }
                } );
            }
        )

        $("#deleteSubmit").click(
            function()
            {
            const form = new FormData()
            
            const elementCode = $("#deleteCodeInput option:selected").text()
            
            form.append("elementCode", elementCode)

            $.ajax( {
                url: 'deleteSubmit',
                type: 'POST',
                data: form,
                contentType: false,
                processData: false,

                success: function() {
                    alert("Success!!!");
                    location.href = 'http://localhost:50102/removeElements.html'
                },
                error: function() {
                    alert("Failure");
                 }
                } );
            }
        )
    } );
  