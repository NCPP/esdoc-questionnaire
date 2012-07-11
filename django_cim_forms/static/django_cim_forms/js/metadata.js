/* custom js for the django_cim application */

///////////////////////

var form_to_add_to = ""
var guid_to_add_to = ""
var model_to_add_to = ""
var app_to_add_to = ""
var field_to_add_to = ""

var id_to_add = ""
var form_to_add = ""

var form_to_remove_from = ""
var guid_to_remove_from = ""
var model_to_remove_from = ""
var app_to_remove_from = ""
var field_to_remove_from = ""

var id_to_remove = ""
var form_to_remove = ""
var button_to_remove_form = ""

/* checks the value of a field (toggler) against an associative array
 * which specifies other fields to toggle based on value */
function toggleStuff(toggler,stuffToToggle) {
    var thisField = $(toggler).parent("div.field");
    var fieldType = $(toggler).attr("type");

    /* TODO: ADD MORE CASES FOR CONDITIONAL ASSIGNMENT (RADIO BOXES, ETC.) */
    var val = (fieldType=="checkbox") ? String($(toggler).is(":checked")) : $(toggler).val();
    
    for (var value in stuffToToggle) {
        var stuff = stuffToToggle[value]
        if (value==val) {
            for (var i=0; i<stuff.length; i++) {
                var selector = "div.field[name='"+stuff[i]+"']";
                $(thisField).find(selector).show();         // look in descendants
                $(thisField).siblings(selector).show();     // and siblings
                selector = "fieldset[name='"+stuff[i]+"']";
                $(thisField).find(selector).show();         // look in descendants
                $(thisField).siblings(selector).show();     // and siblings
            }
        }
        else {
            for (var i=0; i<stuff.length; i++) {
                var selector = "div.field[name='"+stuff[i]+"']";
                $(thisField).find(selector).hide();         // look in descendants
                $(thisField).siblings(selector).hide();     // and siblings
                selector = "fieldset[name='"+stuff[i]+"']";
                $(thisField).find(selector).hide();         // look in descendants
                $(thisField).siblings(selector).hide();     // and siblings

            }
        }
    }
};

function setPropertyTitle(propertyValue) {
    var name = $(propertyValue).parents("div.accordion-content:first").find("div.field[name='longName']").find("input").val();

    // .val()returns the value (shortName), while .text() returns what is actually displayed (longName)
    //var value = $(propertyValue).val();
    // however, I still have to use the .map() fn in order to separate different options with a comma
    var value = $(propertyValue).children("option").filter(":selected").map(function () {
        return $(this).text();
    }).get().join(', ');


    $('select option').map(function () {
  return $(this).text() + ',' + $(this).val();
}).get().join('\n');


    var accordionHeader = $(propertyValue).parents("div.accordion-content:first").prev(".accordion-header");
    var title = name + ": " + value + " ";
    $(accordionHeader).find("a").text(title);
};

function populate(data, form) {
    
    $.each(data, function(key, value){
        if (key=='fields') {
            for (key in value) {
                if (value.hasOwnProperty(key)) {
                    // match all elements with the name of the key (that are children of field)
                    var selector = ".field > [name$='"+key+"']:first";
                    $(form).find(selector).val(value[key]);
                }
            }
        }
    });
};

/*
 * function to determine whether an add dialog box should appear upon pressing the add button
 * (if the addMode is INLINE only, then there is no point displaying the box)
 */
function add_step_zero(row) {
    add_button_type = $(row).closest("fieldset").find(".subform-toolbar > button.add").attr("class");
    if (add_button_type.indexOf("remote") != -1) {
        /* if the set of classes for the add button contains 'remote'... */
        add_step_one(row);
    }
    else {
        return true;
    }
}

function add_step_one(row) {
    var url = window.document.location.protocol + "//" + window.document.location.host + "/metadata/add_form/";
    url += "?g=" + guid_to_add_to + "&a=" + app_to_add_to + "&m=" + model_to_add_to + "&f=" + field_to_add_to;


    $.ajax({
        url : url,
        type : 'get',
        success : function(data) {
            form_to_add = row;
            var content = "<div style='text-align: center; margin-left: auto; margin-right: auto;'>" + data + "</div>";
            $("#add-dialog").html(content);
        }
    });
    $("#add-dialog").dialog("open");
      // ideally, this fn would continue adding content.
      // but the dialog fn doesn't block,
      // so I'm doing this in two steps w/ a callback on the "close" event of the dialog
      return true;
};

function add_step_two() {
    var url = window.document.location.protocol + "//" + window.document.location.host + "/metadata/get_content/";
    url += "?g=" + guid_to_add_to + "&a=" + app_to_add_to + "&m=" + model_to_add_to + "&f=" + field_to_add_to + "&i=" + id_to_add


    $.ajax({
       url : url,
       type : 'get',
       success : function(data) {
            populate($.parseJSON(data),form_to_add);
       }
    });
    return true;
}

/* enable jquery widgets */
function enableJQueryWidgets() {
    $(function() {

       /* enable popup dialogs */
       $("#help-dialog").dialog({autoOpen:false,hide:'explode',modal:true});
       $("#add-dialog").dialog({
            autoOpen:false,hide:'explode',modal:true,
            buttons : {
                ok : function() {
                    id_to_add = $(this).find("select").val();
                    $(this).dialog("close");
                },
                cancel : function() {
                    id_to_add = ""
                    $(this).dialog("close");
                }
            },
            close : function() {
                if (id_to_add != "") {
                    add_step_two();
                }
            }
        });
        $("#remove-dialog").dialog({
            autoOpen:false,hide:'explode',modal:true,
            buttons : {
                ok : function() {
                    $(this).dialog("close");
                },
                cancel : function() {
                    button_to_remove_form = "";
                    $(this).dialog("close");
                }
            },
            close : function() {
                if (button_to_remove_form != "") {
                    $(button_to_remove_form).click();
                }
            }
        });


       /* enable tabs */
       $(".tabs").tabs({
           show : function(event,ui) {
               if ($(ui.tab).attr("class")!="dynamic-formset-initialized") {
                   $(ui.tab).addClass("dynamic-formset-initialized");
                   var tab_selector = $(ui.tab).attr("href");
                   $(tab_selector).find(".accordion").each(function() {
                       var prefix = $(this).attr("class").split(' ')[1];
                       /* the subform+prefix class is added after the multiopenaccordion method below */
                       /* (it's not in the actual template) */
                       var subform_selector = ".subform."+prefix;
                       $(subform_selector).formset({
                           prefix : prefix.split("-formset")[0],
                           added : function(row) {
                               // custom fn to call when user presses "add" for a particular row
                               add_step_zero(row);
                               //add_step_one(row);
                           },
                           // this _needs_ to be completely unique
                           formCssClass : "dynamic-"+prefix
                       });
                   });
               }
           }
       });
       $(".tabs ul li a").keydown(function(event) {
           var keyCode = event.keyCode || event.which;
           if (keyCode == 9) {
               currentTab = $(event.target);
               currentTabSet = $(currentTab).parents("div.tabs:first");
               /* make the tab key shift focus the the next tab */
               var nTabs = $(currentTabSet).tabs("length");
               var selected = $(currentTabSet).tabs("option","selected");
               /* the modulus operator ensures the tabs wrap around */
               $(currentTabSet).tabs("option","selected",(selected+1)%nTabs);               
           }
       });

       /* enable collapsible fieldsets */
       $(".coolfieldset").coolfieldset({speed:"fast"});

       /* enable multi-open accordions */
       $( ".accordion" ).multiOpenAccordion({active:"All"});
       /* have to do this in two steps b/c the accordion JQuery method above cannot handle any content inbetween accordion panes */
       /* but I need a container for dynamic formsets to be bound to */
       /* so _after_ multiopenaccordion() is called, I stick a div into each pane and bind the formset() method to it */
       $(".accordion").find(".accordion-header").each(function() {
           var prefix = $(this).closest(".accordion").attr("class").split(' ')[1];
           var div = "<div class='subform " + prefix + "'></div>";
           $(this).next().andSelf().wrapAll(div);
       });




       /* resize some textinputs */
       $('input[type=text]').each(function(){
           // I could make this dynamic by using the keyup() function instead of each()
           // but, really, I only care about this for property names which are readOnly anyway
           var chars = $(this).val().length;
           $(this).attr("size",chars);               
       });

       /* add functionality to help-buttons (icons masquerading as buttons) */
       $(".help-button").hover (
            function() {$(this).children(".ui-icon-info").addClass('hover-help-icon');},
            function() {$(this).children(".ui-icon-info").removeClass('hover-help-icon');}
       );
       $(".help-button").mouseover(function() {
            $(this).css('cursor', 'pointer');
       });
       $(".help-button").click(function() {
           /* since metadata works with sub-applications, there may be periods in the ids */
           /* I escape them so that javascript doesn't interepret them as class selectors */
           var id = "#" + $(this).attr("id").replace(/(:|\.)/g,'\\$1');
           var x = $(this).offset().left - $(document).scrollLeft();
           var y = $(this).offset().top - $(document).scrollTop();
           var $description = $(id + " > .help-description");
           var title = $description.attr("title");
           var text = $description.html();
           $("#help-dialog").html(text);
           $("#help-dialog").dialog("option",{title: title, position: [x,y], height: 200, width: 400}).dialog("open");
           return false;
       });

        /* enable enumeration widgets */
        /* (these are multiwidgets: a choice and a textfield) */
        /* (the latter is only shown when the former is set to "OTHER") */
        $(".enumeration-value").each(function() {
            enumerationValue = $(this);
            //enumerationOther = enumerationValue.next(".enumeration-other");
            enumerationOther = enumerationValue.siblings(".enumeration-other:first");

            if (enumerationValue.attr("multiple")=="multiple") {
                multipleValues = enumerationValue.val();
                // TODO: CHECK THE INDEXOF FN IN IE                
                if (! multipleValues || multipleValues.indexOf("OTHER")==-1) {
                    enumerationOther.hide();
                }
                else {
                    enumerationOther.show();
                }
                
                /* if NONE is selected, then all other choices should be de-selected */
                if ( multipleValues && multipleValues.indexOf("NONE") != -1) {
                    enumerationValue.val("NONE")
                    enumerationOther.hide();
                }
            }
            else {
                if (enumerationValue.val()=="OTHER") {
                    enumerationOther.show();
                }
                else {
                    enumerationOther.hide();
                }
            }
            
            // position the "other" textbox relative to the "value" select
            enumerationOther.before("<br/>");
            $(enumerationOther).offset({
                "left" : $(enumerationValue).offset().left
            });

        });        
        $(".enumeration-value").change(function(event) {
            enumerationValue = $(event.target);
            //enumerationOther = enumerationValue.next(".enumeration-other");
            enumerationOther = enumerationValue.siblings(".enumeration-other:first");
            if (enumerationValue.attr("multiple")=="multiple") {
                multipleValues = enumerationValue.val();
                // TODO: CHECK THE INDEXOF FN IN IE
                //if (! multipleValues || multipleValues.indexOf("OTHER")==-1) {
                if (multipleValues.indexOf("OTHER")==-1) {
                    enumerationOther.hide();
                }
                else {
                    enumerationOther.show();
                }
                
                /* if NONE is selected, then all other choices should be de-selected */
                if ( multipleValues && multipleValues.indexOf("NONE") != -1) {
                    enumerationValue.val("NONE")
                    enumerationOther.hide();
                }


            }
            else {
                if (enumerationValue.val()=="OTHER") {
                    enumerationOther.show();
                }
                else {
                    enumerationOther.hide();
                }
            }
            
            // position the "other" textbox relative to the "value" select            
            $(enumerationOther).offset({
                "left" : $(enumerationValue).offset().left
            });
        });
        

        /* custom code to disable a widget (used when field is customized to 'readonly') */
        /* turns out that disabling it directly in Django causes the value to be set to None,
         * which means, the incorrect value is saved */
        $(".disabled").each(function() {
  
            // I AM HERE
            $(this).attr('disabled','true');

        });

        /* init an 'enabler' - a field that controls other fields or forms */
        $(".enabler:not(.enumeration-other)").each(function() {
            // the onchange method is bound to the toggleStuff function
            $(this).trigger("change");
        });

        /* enable calendar widgets */
        $(".datepicker").datepicker(
            {changeYear : true, showButtonPanel : true, showOn : 'button', buttonImage : '/static/django_cim_forms/img/calendar.gif'}
        );
        $(".ui-datepicker-trigger").mouseover(function() {
            $(this).css('cursor', 'pointer');
        });
        $(".ui-datepicker-trigger").attr("title","click to select date");
        $(".ui-datepicker-trigger").css("vertical-align","middle");

        /* enable _fancy_ buttons */
        $(".button").button();
        $(".subform-toolbar button").mouseover(function() {
            $(this).css('cursor', 'pointer');
        });
        $(".subform-toolbar button.expand" ).button({
             icons : {primary: "ui-icon-circle-triangle-s"},
             text : false,
        }).click(function(event) {
        // TODO: THIS IS NO LONGER WORKING B/C THERE IS CONTENT BETWEEN ACCORDIONS
            var formset = $(event.target).closest("fieldset");
            var accordion = $(formset).find(".accordion:first");
            $(accordion).multiOpenAccordion("option","active","All");
        });
        $(".subform-toolbar button.collapse" ).button({
            icons : {primary: "ui-icon-circle-triangle-n"},
            text: false,
        }).click(function(event) {
        // TODO: THIS IS NO LONGER WORKING B/C THERE IS CONTENT BETWEEN ACCORDIONS
            var formset = $(event.target).closest("fieldset");
            var accordion = $(formset).find(".accordion:first");
            $(accordion).multiOpenAccordion("option","active","None");
        });
        $("button.remove").button({
            icons: {primary: "ui-icon-circle-minus"},
            text: false,
        });
        $("button.remove").bind("click", function(e) {
            /* prevent the delete button from _actually_ opening the accordian tab */
            e.stopPropagation();
        });
        $("button.remove").click(function(event) {

            
            var fieldset = $(event.target).closest("fieldset");
            var subform = $(event.target).closest(".subform");

            model_to_remove_from = $(fieldset).find("span.current_model:first").text();
            field_to_remove = $(fieldset).find("span.current_field:first").text();

            button_to_remove_form = $(subform).find(".delete-row");

            var content = "<div style='text-align: center; margin-left: auto; margin-right: auto;'>Do you really wish to remove this instance of " + field_to_remove + "?<p><em>(It will not be deleted, only removed from this " + model_to_remove_from + ")</em></p></div>";
            $("#remove-dialog").html(content);
            $("#remove-dialog").dialog("open");

//            $(button_to_remove_form).click();

        });
        $(".subform-toolbar button.add").button({
            icons: {primary: "ui-icon-circle-plus"},
            text: false,
        }).click(function(event) {
            
            fieldset = $(event.target).closest("fieldset");

            // there are two situations where I can be adding/replacing content
            // either a subForm or a subFormSet
            if ($(event.target).hasClass("FORM")) {
                form_to_add = $(fieldset);

            }
            else {
                // form_to_add is set in add_step_one
            }

            guid_to_add_to = $(fieldset).find("span.current_guid:first").text();
            model_to_add_to = $(fieldset).find("span.current_model:first").text();
            app_to_add_to = $(fieldset).find("span.current_app:first").text();
            field_to_add_to = $(fieldset).find("span.current_field:first").text();

            var add_button = $(fieldset).find(".add-row:first");
            $(add_button).click();

        });
    });
};
