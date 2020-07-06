Changes have been made to the web2py.js handles the Flash html element. New code is shown below:

        /* My Changes Below */
        flash: function (message, status) {
            var flash = $('.w2p_flash');
            web2py.hide_flash();
            flash.text(message).addClass(status);
            
            var AutoCloseFlash = true;

            if (message.toLowerCase().substring(0,7)=='success') { 
                flash.text(message).addClass('bg-success');
                flash.text(message).removeClass('bg-danger');
                flash.text(message).addClass('text-white');

            } else if (message.toLowerCase().substring(0,5)=='error') { 
                flash.text(message).addClass('bg-danger');
                flash.text(message).removeClass('bg-success');
                flash.text(message).addClass('text-white');
                AutoCloseFlash = false;
            } else {
                flash.text(message).removeClass('bg-danger');
                flash.text(message).removeClass('bg-success');
                flash.text(message).removeClass('text-white');
            }
            if (flash.html()) flash.append('<span id="closeflash"> &times; </span>')[animateIn]();
            if (AutoCloseFlash) {setTimeout('jQuery(".w2p_flash").fadeOut("slow")',5000);}
        },
        /* End of My Changes */
