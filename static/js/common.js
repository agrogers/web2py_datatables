
// -------------------------------------------------------------------------------------------------------
//                                Miscellaneous
// -------------------------------------------------------------------------------------------------------
function Get_URL(Controller,Function, Args="", Vars="") {

    url = URL_CF.replace('C',Controller).replace('F',Function);
    if (Args != "") {url += `/${Args}`}
    if (Vars != "") {
        if (Vars.constructor == Object) {
            // This is a dictionary so build vars
            vars = ''
            for (var k in Vars) {
                if (vars != '') {vars += '&'};
                vars += `${k}=${Vars[k]}`;
            }
            Vars = vars;
        } 
        url += `?${Vars}`
    }
    return  url
}
function RenderFormParts() {

    $('.multiSelect').multiSelect({
        selectableHeader: "<input type='text' class='search-input' autocomplete='off' placeholder=''>",
        selectionHeader: "<input type='text' class='search-input' autocomplete='off' placeholder=''>",
        afterInit: function(ms){
          var that = this,
              $selectableSearch = that.$selectableUl.prev(),
              $selectionSearch = that.$selectionUl.prev(),
              selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
              selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';
      
          that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
          .on('keydown', function(e){
            if (e.which === 40){
              that.$selectableUl.focus();
              return false;
            }
          });
      
          that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
          .on('keydown', function(e){
            if (e.which == 40){
              that.$selectionUl.focus();
              return false;
            }
          });
        },
        afterSelect: function(){
          this.qs1.cache();
          this.qs2.cache();
        },
        afterDeselect: function(){
          this.qs1.cache();
          this.qs2.cache();
        }
      });    
}

//-------------------------------------------------------------------------------
//                             Numeric functions
//-------------------------------------------------------------------------------

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

//-------------------------------------------------------------------------------
//                             String functions
//-------------------------------------------------------------------------------
// Extracts the 'src' attribute value from a string
function extractSrc(str){
    var regex = /<img.*?src='(.*?)'/;
    var src = regex.exec(str);
    console.log(src);
        if (src == null) {
            regex = /<img.*?src="(.*?)"/;
            src = regex.exec(str);
        }
        if (src == null) 
        {return '' }
        {return src[1];}
};

//-------------------------------------------------------------------------------
//                             DOM Element functions
//-------------------------------------------------------------------------------
function ShowHideSection(ElementToShow){
    //var e = document.getElementById(ElementToShow);
    //e.toggle();
    $("#" + ElementToShow).toggle();
};
