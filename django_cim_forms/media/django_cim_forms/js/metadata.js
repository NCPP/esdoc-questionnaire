/* custom js for the django_cim application */

function removeForm(data) {
  alert(data);
};


///////////////////////

var form_to_add_to = ""

var guid_to_add_to = ""
var model_to_add_to = ""
var app_to_add_to = ""
var field_to_add_to = ""

var id_to_add = ""


// TODO:
function toggleStuff(toggler,stuff) {
    var checked = $(toggler).attr("checked");
    
    var len=stuff.length;
    for(var i=0; i<len; i++) {
        var thisStuff = stuff[i];
        var selector = "*[name="+thisStuff+"]";
        if (checked) {
            $(selector).show();
        }
        else {
            $(selector).hide();
        }
        //$(selector).toggle();
    }
};

function populate(data, form) {
    $.each(data, function(key, value){
        if (key=='fields') {
            for (key in value) {
                if (value.hasOwnProperty(key)) {
                    var selector = "[name$='"+key+"']:first";
                    $(form).find(selector).val(value[key]);
                }
            }
        }
    });
};

function add_step_one() {
    var url = window.document.location.protocol + "//" + window.document.location.host + "/metadata/add_form/";
    url += "?g=" + guid_to_add_to + "&a=" + app_to_add_to + "&m=" + model_to_add_to + "&f=" + field_to_add_to;

    $.ajax({
        url : url,
        type : 'get',
        success : function(data) {
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


       /* enable tabs */
       $(".tabs").tabs();

       /* enable collapsible fieldsets */
       $(".coolfieldset").coolfieldset({speed:"fast"});

       /* enable multi-open accordions */
       $( ".accordion" ).multiOpenAccordion({active:"All"});

       /* resize some textinputs */
       $('input[type=text]').each(function(){
           // I could make this dynamic by using the keyup() function instead of each()
           // but, really, I only care about this for property names which are readOnly anyway
           var chars = $(this).val().length;
           $(this).attr("size",chars);               
       });

       /* add functionality to help-buttons (icons masquerading as buttons) */
       $(".help-button").hover (
            function() { $(this).children(".ui-icon-info").addClass('hover-help-icon'); },
            function() { $(this).children(".ui-icon-info").removeClass('hover-help-icon'); }
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
            enumerationOther = enumerationValue.next(".enumeration-other");
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
        });
        $(".enumeration-value").change(function(event) {
            enumerationValue = $(event.target);
            enumerationOther = enumerationValue.next(".enumeration-other");
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
        });

        /* init an 'enabler' - a boolean that controls other elements */
        $(".enabler").bind("click",toggleStuff);
        $(".enabler").each(function() {
            $(this).trigger("click");
            /*
            if ($(this).is(".start-enabled")) {
                $(this).attr("checked","checked");
            }
            else {
                $(this).removeAttr("checked");
            }*/
        });

        /* enable calendar widgets */
        $(".datepicker").datepicker(
            { changeYear : true, showButtonPanel : true, showOn : 'button', buttonImage : '/site_media/django_cim_forms/img/calendar.gif' }
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
             icons : { primary: "ui-icon-circle-triangle-s" },
             text : false,
        }).click(function(event) {
        // TODO: THIS IS NO LONGER WORKING B/C THERE IS CONTENT BETWEEN ACCORDIONS
            var formset = $(event.target).closest("fieldset");
            var accordion = $(formset).find(".accordion:first");
            $(accordion).multiOpenAccordion("option","active","All");
        });
        $(".subform-toolbar button.collapse" ).button({
            icons : { primary: "ui-icon-circle-triangle-n" },
            text: false,
        }).click(function(event) {
        // TODO: THIS IS NO LONGER WORKING B/C THERE IS CONTENT BETWEEN ACCORDIONS
            var formset = $(event.target).closest("fieldset");
            var accordion = $(formset).find(".accordion:first");
            $(accordion).multiOpenAccordion("option","active","None");
        });
        $("button.remove").button({
            icons: { primary: "ui-icon-circle-minus" },
            text: false,
        });
        $("button.remove").bind("click", function(e) {
            /* prevent the delete button from _actually_ opening the accordian tab */
            e.stopPropagation();
        });
        $(".subform-toolbar button.add").button({
            icons: { primary: "ui-icon-circle-plus" },
            text: false,
        }).click(function(event) {
            
            fieldset = $(event.target).closest("fieldset");

            // there are two situations where I can be adding/replacing content
            // either a subForm or a subFormSet
            if ($(event.target).hasClass("FORM")) {
                form_to_add = $(fieldset);
            }
            else {
                alert("you clicked add on a FORMSET")
            }

            guid_to_add_to = $(fieldset).find("span.current_guid:first").text();
            model_to_add_to = $(fieldset).find("span.current_model:first").text();
            app_to_add_to = $(fieldset).find("span.current_app:first").text();
            field_to_add_to = $(fieldset).find("span.current_field:first").text();

            add_step_one();
        });
    });
};