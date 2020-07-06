function DatatableGrid(init_dt_settings, init_TargetElement){

    var _this = this;
    var _Element = null;
    var _ElementID = null;
    var _ElementIDname = null
    var AddURL = null;
    var EditURL = null;
    var Table                       // Refers to the DataTable object
    this.CurrentID = null;          // Holds the ID of the currently selected row
    this.Data = null       // Holds an object with current Datatable record
    var RefreshingTableAfterAjaxCall = false; // Needed to ensure we dont refresh the subform more than once.
    var GridDataCriteria = { CardMasterID : 0, Action : '', DeckID : 0, ListOfDecks:[] };
    var CurrentAction = null;
    var DT_Settings;
    var DisabledFields;
    this.Event_RowSelected = null;
    this.Event_initComplete = null;

    this.Initialise = function (dt_settings, TargetElement) {
        DT_Settings = dt_settings;
        CurrentTableName = DT_Settings.TableName    // A global variable - initialised in show.html

        _DT_ContainerIDname = TargetElement;
        _DT_ContainerID = `#${TargetElement}`; 

        $(_DT_ContainerID).html(DT_Settings.html);

        _Element = $(_DT_ContainerID).find(".web2py-datatable").first();
        _ElementIDname = _Element.attr("id");
        _ElementID = `#${_ElementIDname}`;

        // Set the headings and icon
        if (dt_settings.Icon == null) {
            $(`${_ElementID}-datatable-icon`).remove()
        } else {
            $(`${_ElementID}-datatable-icon`).html(dt_settings.Icon);
        }
        $(`${_ElementID}-datatable-heading1`).html(dt_settings.PageHeading);
        if (dt_settings.PageSubHeading == "") {
            $(`${_ElementID}-datatable-subheading1`).remove()
        } else {
            $(`${_ElementID}-datatable-subheading1`).html(dt_settings.PageSubHeading);
        }
        if (dt_settings.Info == null) {
            $(`${_ElementID}-datatable-info`).remove()
        } else {
            $(`${_ElementID}-datatable-info`).html(dt_settings.Info);
        }
        
        // Set default urls for add and edit
        AddURL = `/smartdeck/datatable/add/${DT_Settings.DataTableName}`
        EditURL = `/smartdeck/datatable/edit/${DT_Settings.DataTableName}/{id}`

        if (DT_Settings.AddURL!='') {if (DT_Settings.AddURL == 'IncludeVars') {AddURL = AddURL + '?{VARS}' } else {AddURL = DT_Settings.AddURL}}
        if (DT_Settings.EditURL!='') {if (DT_Settings.EditURL == 'IncludeVars') {EditURL = EditURL + '?{VARS}' } else {EditURL = DT_Settings.EditURL}}

        if (DT_Settings.Tabs != null) {
            TabsAdding = DT_Settings.Tabs;
            TabsEditing = DT_Settings.Tabs;
        } 
        if (DT_Settings.TabsAdding != null) {TabsAdding = DT_Settings.TabsAdding};
        if (DT_Settings.TabsEditing != null) {TabsEditing = DT_Settings.TabsEditing};

        RowID = null;
        if (DT_Settings.Responsive) {Responsive={details: { type: 'column'}} } else {Responsive=false};
        Table  = _Element.DataTable( {
            dom: dt_settings.DOM,
            data: dt_settings.data,
            deferRender: true,
            rowId: 'ID',
            pageLength: DT_Settings.PageLength,
            buttons: [], //['selectAll','excel','print','colvis'],
            order: dt_settings.order,
            columns: dt_settings.columns,
            columnDefs: dt_settings.columnDefs,
            select: {style: 'single', toggleable: false },
            responsive: Responsive,
            autoWidth: false,
            stateSave: true,  // The page 'state' doesnt seem to be restored after the table has been dynamically restored.
            stateSaveParams: function(settings, data) {
                data.columns.forEach(function(column) {
                delete column.visible;})},
            fixedHeader: {footer: true},
            initComplete: function(settings, json) {initComplete()},
            drawCallback: function( settings ) {
                /*alert( 'DataTables has redrawn the table' ) */;                   
            },
            createdRow: function (row, data, dataIndex, cells) {
            }
        } )
        // Add the column search input boxes
        i = 0;
        $(`${_ElementID} tfoot th`).each( function () {
            fld = dt_settings.Fields[i];
            if (fld in dt_settings.SearchFieldSize) {
                size = dt_settings.SearchFieldSize[fld]
            } else {
                size = 15;
            }
            if (dt_settings.Searchable.includes(fld)) {
                var title = $(this).text();
                $(this).html( `<input class="search" size="${size}" type="text" placeholder="" />` );
            } else {
                $(this).html('');
            }
            i += 1
        } );
        // Hide control header text
        $(`${_ElementID} thead th`).each( function () {
            var title = $(this).text();
            if (title.charAt(0) == ":") {
                $(this).html('');
            }
        } );
        // Apply the search
        Table.columns().every( function () {
            var that = this;
            $( 'input', this.footer() ).on( 'keyup change clear', function () {
                if ( that.search() !== this.value ) {
                    that
                        .search( this.value )
                        .draw();
                }
            } );
        } );
        // Move the search row from the footer to the header
        $(`${_ElementID} tfoot tr`).appendTo(`${_ElementID} thead`);
        // Restore state
        var state = Table.state.loaded();
        if (state) {
            Table.columns().eq(0).each(function (colIdx) {
                var colSearch = state.columns[colIdx].search;
                if (colSearch.search) {
                    $('input', Table.column(colIdx).footer()).val(colSearch.search);
                }
            });
            Table.draw();
        }
        // Add the required buttons
        (dt_settings.Buttons).forEach(function (item, index) {
            if (item == 'Add') {
                Table.button().add( 0, {
                    text: "Add", //data-action="Add" 
                    action: function ( e, dt, node, config ) {
                        HandleTableEvent('add');
                        // No function is needed to show the Modal because it is controlled by the data attributes
            }})}
            if (item == 'Edit') {
                Table.button().add( 0, {
                    text: 'Edit',
                    extend: "selectedSingle",
                    action: function ( e, dt, node, config ) {
                        CurrentAction = 'edit';
                        AddOrEditRecord('', _this.CurrentID);}
                })}
            if (item == 'Delete') {
                Table.button().add( 0, {
                    text: 'Delete',
                    extend: "selectedSingle",
                    action: function ( e, dt, button, config ) {
                        HandleTableEvent('delete', null, _this.CurrentID);}
            })};
        })
        // Attach events to the table
        Table.on( 'select', function () {
            var selected = Table.rows( { selected: true } );
            d = selected.data();
            _this.Data = d[0]
            if ( selected.any() ) {
                RowID = selected[0][0]
                _this.CurrentID = selected.data()[0].ID;    // I want to use the rowId but it is always undefined!
                CurrentTableName = DT_Settings.TableName    // A global variable - initialised in show.html
                Current_id = _this.CurrentID                // A global variable - initialised in show.html
                            
                if (typeof _this.Event_RowSelected === "function") {_this.Event_RowSelected(_this);}
            }
        } );
        // Attach click events to edit and submit  buttons. 
        _Element.on("click", ".edit-icon", function (event) {
            HandleTableEvent('edit', null, $(this).attr('RowID'))
        })
    } // Initialise

    function initComplete() {
        if (typeof _this.Event_initComplete === "function") {_this.Event_initComplete(_this);}
    }
    function RefreshGrid(Criteria = null) {
        GridDataCriteria = Criteria;
        //SetTableDataSource();
        Table.ajax.reload();
    } 
    function GetTable(){
        return Table
    }
    function SetGridDataCriteria(Criteria){
        GridDataCriteria = Criteria;
    }
    this.submit = function() {
        submitForm()
    }
    this.submitForm = function() {
        if (CurrentAction == 'edit') {
            url = `${EditURL}`;
        } else {
            url = `${AddURL}`;
        }
        
        EnableOrDisableInputs(true,DisabledFields);  // Re-enable the disabled fields. We do it this way because web2py will not write a disabled field to the database. This is problem when adding a record because we need the disabled fields to be persisted
        
        url = ParseURL(url, _this.CurrentID);
        FormElement = `${_ElementID}-dialog-form`;
        Options = {success: function(data, textStatus) {
                        EnableOrDisableInputs(false,DisabledFields); // Disable controls
                        result = JSON.parse(data);
                        if (result.Success) {
                            UpdatedRecord = result.record;
                            
                            if (CurrentAction == 'edit') {
                                Table.row(RowID).data(UpdatedRecord).draw('full-hold');
                                SendUploadFileToServer(url, result.id);  // Check if we need to save any files. This can be done via the standard AJAX method so do separately. Something about multipart forms.

                            } else {
                                SendUploadFileToServer(url, result.id);  // Check if we need to save any files. This can be done via the standard AJAX method so do separately. Something about multipart forms.
                                // Adding record
                                Table.row.add(UpdatedRecord);
                                Table.order([dt_settings.IDcolumnNumber,'desc']);
                                Table.draw();
                            }
                            // alert("Success!" + data);
                            $(`${_ElementID}-dialog`).modal('hide');
                        } else {
                            alert('Something didnt  work out.');
                        }
                    },
                    error: function(data,textStatus) {
                        EnableOrDisableInputs(false,DisabledFields); // Disable controls
                    }
                }
        ajax(url, FormElement, '', Options);
    
        return false; //Need this to override the default  behaviour of the standard form Submit button
    }
    function EnableOrDisableInputs(Enable=true, FieldList) {
        FieldList.forEach(function(item,index) {
            if (Enable) {
                $(`#${item}`).removeAttr('disabled');
            } else {
                $(`#${item}`).attr('disabled','');
            }
        })

    }
    function ParseURL(url, ID) {
        url = url.replace('{id}', ID);
        url = url.replace('?{VARS}', window.location.search)
        return url
    }
    function AddOrEditRecord(Target, ID=null) {
        Target = `${_ElementID}-dialog`  // Multiple grids are allowed per page. Just make sure the ElementID's specified are unique - or specify no ID and let one be assigned at random.
        FormElement = `${_ElementIDname}-dialog-form`;
        FormElementDiv = $(`#${FormElement}-div`);  
        FormElementDiv.html("Loading...");

        $(Target).modal('show');
        if (CurrentAction == 'edit') {
            url = `${EditURL}`;
            Tabs = TabsEditing;
        } else {
            _this.CurrentID = null;
            url = `${AddURL}`;
            Tabs = TabsAdding;
        }
        url = ParseURL(url, ID);
        vars = DT_Settings.vars;
        // json_vars = JSON.stringify({'TableVars':vars}),
        json_vars = JSON.stringify(vars),
        $.ajax({url: url,
                dataType: 'json', // The datatype of the result. json for objects, remove for HTML
                contentType: 'application/json; charset=utf-8',
                data: json_vars,
                type: 'POST',
                success: function(result){
                    // Put the returned form into the correct location on the page.
                    FormElementDiv.html(result.form);  
                    form = FormElementDiv.children('form');
                    form.attr('id',FormElement);
                    if (Tabs != null) {AddTabs(FormElementDiv, Tabs);}
                    // Disable the requested fields. We do it this way because web2py, when building the form, will hide controls that are not writable. But usually i want to see that field so i know exactly when i am adding too.
                    DisabledFields = result.DisabledFields;
                    EnableOrDisableInputs(false,DisabledFields);
                    RenderFormParts();  // Applies any special rendering like building the special multiselect list select (file common.js)
                    $(`${_ElementID}-dialog`).off("click", ":submit");  // Make sure there are no existing handlers on the dialog. This is needed on the second and subsequent openings of the dialog
                    $(`${_ElementID}-dialog`).on("click", ":submit", function (event) {_this.submitForm();})            
                }})    
    }
    function DeleteRecord(ID){
        if (ID == null) {
            alert("The record ID is not known so the record cannot be deleted.")
        } else {
            OKtoDelete = confirm(`Are you sure you want to delete record '${ID}'`);
            if (OKtoDelete) {
                
                // Table.rows( { selected: true } )[0].remove();
                // Table.draw(false);

                url = `/smartdeck/datatable/delete/${dt_settings.DataTableName}/${ID}`;
                $.ajax({url: url,
                        success: function(result){
                            result = JSON.parse(result);
                            if (result.Deleted) {
                                Table.row('.selected').remove().draw( false );
                            }
                            if (!(result.Success)) {
                                alert("PROBLEM: " + result.message)
                            }
                            $(`${_ElementID}-dialog`).modal('hide');
                        }})    
            }

        }
    }
    function HandleTableEvent(Action, Target = null, ID = null) {
        CurrentAction = Action;
        if (Action == "edit" | Action == "add") {
            AddOrEditRecord(Target, ID);
        } else if (Action == "delete") {
            DeleteRecord(ID);
        }

        // alert(Action + " = " + Target);
    }
    function AddTabs(FormElementDiv, Tabs) {

        // var $set = $("#nav-tabContent").children(".form-group");
        var $set = $(`${_ElementID}-dialog-form`).find(".form-group");
        TabLabels = [];
        html = '';
        LastFieldNumber = 1;
        if (Array.isArray(Tabs)) {
            // An array describing  the tab structure has been passed in
            if (!isNaN(Tabs[0].Field)) {
                // The Field is a number so assume we are working with index of fields not field names
                UsingFldIndexes = true;
            } else {
                UsingFldIndexes = false;
            }
            TabPageTotal = Tabs.length;
            for (i=1; i<=TabPageTotal; i++) {
                Tab = Tabs[i-1];
                if (UsingFldIndexes) {
                    Tab.FieldNumber = parseInt(Tabs[i-1].Field-1,10) // Field indexes are supplied with base 1, not 0.
                } else {
                    Tab.FieldNumber = DT_Settings.ModelFields.indexOf(Tabs[i-1].Field);
                }
                if (Tab.FieldNumber < LastFieldNumber) {Tab.FieldNumber = LastFieldNumber+1};
                TabLabels.push(Tab);
                LastFieldNumber = Tab.FieldNumber
            }
            TabClass = 'labeled-tabs'

        } else {
            // Build an array to use
            FieldsPerPage = 6;
            FieldCnt = $set.length - 1;  // The submit row is included in this set
            TabPageTotal = Math.ceil(FieldCnt/FieldsPerPage);
            // url_tab_icon = URL_icon_set + '/svg/tab_icon.svg'
            // tab_img = `<img src="${url_tab_icon}" style="width:16px">`
            for (i=1; i<=TabPageTotal; i++) {
                var T = {}
                T.Field = i.toString();
                T.Label = i.toString();
                T.FieldNumber = FieldsPerPage * (i-1);
                if (T.FieldNumber < LastFieldNumber) {T.FieldNumber = LastFieldNumber+1};
                TabLabels.push(T)
                LastFieldNumber = T.FieldNumber
            }
            TabClass = 'numbered-tabs'
        }
        if (TabPageTotal==1){return} // If there is only one tab then show it without tabs
        cnt = 0;
        for (i=0; i<TabPageTotal; i++) {
            cnt += 1
            if (cnt==1) {Active = 'active'} else {Active=''};
            html += `<a class="nav-item nav-link ${Active}" id="nav-${cnt}-tab" data-toggle="tab" href="#nav-${cnt}" role="tab" aria-controls="nav-${cnt}" aria-selected="true"><span class="${TabClass}">${TabLabels[i].Label}</span></a>`
        }

        header = `
        <nav>
            <div class="nav nav-tabs" id="nav-tab" role="tablist">${html}</div>
        </nav>`
        
        $(`${_ElementID}-dialog-form`).prepend(header);

        $(FormElementDiv).find(".form-group").wrapAll(`<div class="tab-content" id="nav-tabContent" />`);

        cnt = 0;

        LastFieldNumber = 0;
        for(var i=0, len = TabPageTotal; i < len; i++){
            cnt += 1;
            if (cnt==1) {
                Active = 'active';
                FromField = 0;
                ToField = TabLabels[i+1].FieldNumber
            } else {
                Active=''
                FromField = TabLabels[i].FieldNumber;
                if (cnt==TabPageTotal) {
                    ToField = $set.length;
                } else {
                    ToField = TabLabels[i+1].FieldNumber
                }
            }
            $set.slice(FromField, ToField).wrapAll(`<div style="padding-top: 10px" class="tab-pane fade show ${Active}" id="nav-${cnt}" role="tabpanel" aria-labelledby="nav-${cnt}-tab" />`);
        }    
        
        return;
    }
    function SendUploadFileToServer(URL, id) {

        var formElem = $(".sd-form");  // Get the smartdeck form(s)
        if (formElem != null) {
            $(".input-file.upload").each(function() {
                file = this.files[0];
                if (file != null) {
                    var formData = new FormData(formElem[0]);
                    var request = new XMLHttpRequest();
                    formData.set('file', file);
                    formData.set('TableName', DT_Settings.TableName);
                    formData.set('FieldName', $(this).attr('name'));
                    formData.set('id', id);
                    request.open("POST", URL + '/UploadFile/');
                    request.send(formData);                
                }
            })
        }
        
    

    };    
    this.GetCurrentID = function() {
        return  _this.CurrentID;
    }
    Object.defineProperties(this, { // defines ElementID (initialises the HTML for the card), FaceUp, AnswerVisible, QuestionVisible, Buttons and more. These properties are required to do other stuff when they are set.
        "xElementID": { // string holding the name of the HTML element. Used to find the element '#cardcol-{ElementID}' which is where the html goes for this card.
          "get": function() {
              return this._ElementID},
          "set": function(x) { 
              this._ElementID = x;
              ColElementName = "cardcol-" + x;
              this.ColumnElement = document.getElementById(ColElementName);  // This is the column element that the card will be placed into.
              if (this.ColumnElement == null) {
                alert(`Could not find html element "${ColElementName}".`)
              } else {
              }
            }  
        }
    }) // End of defineProperties    

    // Process variables passed in when creating object
    if (init_dt_settings != null && init_TargetElement != null){this.Initialise(init_dt_settings, init_TargetElement)}

}  // End of Datatable Object Definition
//=====================================================================================================

