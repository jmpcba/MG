/*global WildRydes _config*/

var WildRydes = window.WildRydes || {};
WildRydes.map = WildRydes.map || {};

(function rideScopeWrapper($) {
    var authToken;
    WildRydes.authToken.then(function setAuthToken(token) {
        if (token) {
            authToken = token;
        } else {
            window.location.href = '/signin.html';
        }
    }).catch(function handleTokenError(error) {
        alert(error);
        window.location.href = '/signin.html';
    });


    function enviarMail(pickupLocation) {

        var URL = "https://8slcpf2nkc.execute-api.us-east-1.amazonaws.com/prod/v1/presupuesto"
        var items = []
        console.log($(".entradas").length)
        $(".entradas").each(function (i, element) {

            var cant = $(element).find("[id^=txtCant]").val()
            var unit = $(element).find("[id^=txtUnitario]").val()
            var prod = $(element).find("[id^=txtProducto]").val()
            var tot = $(element).find("[id^=txtTotal]").val()

            var presupuesto = {
                producto: prod,
                cantidad: cant,
                unitario: unit,
                total: tot
            }
            items.push(presupuesto)
        })
        
        var data = {
            mail: $("#txtMail").val(),
            presupuestos: items
        }

        console.log(data)
        console.log(items)

        $.ajax({
            type: "POST",
            url: URL,
            headers: {
                'Access-Control-Allow-Origin': '*',
                Authorization: authToken,
            },
            dataType: "json",
            crossDomain: "true",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data),


            success: function () {
                // clear form and show a success message
                alert("Presupuesto enviado a: " + data.mail);
                $("#frmPresupuesto")[0].reset();
                //location.reload();
            },

            error: function (xhr, status, error) {
                var err = eval("(" + xhr.responseText + ")");
                alert(err.Message);
            }
        });
    }

    // Register click handler for #request button
    $(function onDocReady() {
        $('#btnEnviar').click(handleRequestClick);

        WildRydes.authToken.then(function updateAuthMessage(token) {
            if (token) {
                $('.authToken').text(token);
            }
        });

        if (!_config.api.invokeUrl) {
            $('#noApiMessage').show();
        }
    });

    function handleRequestClick(event) {
        event.preventDefault();
        enviarMail();
    }
}(jQuery));
