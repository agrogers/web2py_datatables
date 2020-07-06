The application has one user: admin and password: admin

I don't think you need to be logged in to access the /application/datatables/show

The files you need to make the integration work are:

controllers 
> datatable.py

models
> common_datatables.py
> common_functions_public.py

static
> css
>> multi-select.css
>> web2py-datatables.css

>img
>> switch.png
>> icons\set1\svg\expand.svg
>> icons\set1\svg\edit-pencil.svg

>js
>> datatable\datatable_web2py.js
>> common.js
>> imagepicker.js
>> jquery.multi-select.js
>> jquery.quicksearch.js
>> web2py.js (optional - slightly modified)

views
> datatable
>> add.html, edit.html (not sure why I need these. I don't want them)
>> files.load
>> show.html


