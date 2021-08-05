odoo.define('matco_hr_attendance_portal.Attendance', function(require) {
    "use strict";
    var rpc = require("web.rpc");
    var ajax = require('web.ajax');
$(document).ready(function() {

      $('#datetimepicker').datetimepicker({
            toolbarPlacement: "bottom",
            icons :{
                'close' : "fa fa-check"
            },
            buttons :  {
                showClose :  true
            }
          });

      $('#datetimepicker_end').datetimepicker({
            toolbarPlacement: "bottom",
            icons :{
                'close' : "fa fa-check"
            },
            buttons :  {
                showClose :  true
            }
          });

    $('#project_ids').change(function(){
        ajax.jsonRpc('/attendance/employee','call',{
        id: parseInt(document.getElementById('project_ids').value)}).then(function (data)
        {
            var selectEmployee = $("select[name='employee']");
            var selectTask = $("select[name='project_task']");
            selectEmployee.html('');
            selectTask.html('');
            selectEmployee.append('<option value="none" selected disabled>Select Employee</option>')
            for(var i = 0;i<Object.values(data['employee_id']).length;i++)
            {
                var opt = '<option value='+Object.keys(data["employee_id"])[i]+'>'+Object.values(data["employee_id"])[i]+'</option>'
                selectEmployee.append(opt);
            }
            selectTask.append('<option value="none" >Select Task</option>')
            for(var i = 0;i<Object.values(data['task_id']).length;i++)
            {
                var opt_task = '<option value='+Object.keys(data["task_id"])[i]+'>'+Object.values(data["task_id"])[i]+'</option>'
                selectTask.append(opt_task);
            }
        });
    });


    $('#employee_id').change(function(){
        ajax.jsonRpc('/attendance/planning_slot','call',{
        employee_id: parseInt($('#employee_id').val()),'project_id' : parseInt($('#project_ids').val())}).then(function (data)
        {
                if(data != false)
                {
                     document.getElementById('date_start').value = data['start_datetime']
                     document.getElementById('date_end').value = data['end_datetime']
                }
        });
    });

    var date_end  = document.getElementById('date_end')
    console.log('5555555555555555555555555',date_end)
    $('#calculate_days').click(function(){
        if ($("#date_start").val() != "" && $("#date_end").val() != "")
        {
            var Days = 0;
            var date1 = new Date($("#date_start").val());
            var date2 = new Date($("#date_end").val());
            var total_hour = date2 - date1
            const diffTime = Math.abs(date2 - date1);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            console.log('3333333333333333333',diffDays)
//            var d = moment.duration(total_hour, 'milliseconds');
//            var hours = Math.floor(d.asHours());
//            Days=Math.floor(hours/24);
//            var hours_minute = d/(3600*1000)
//            console.log("-------------------------------",Days)
            if (diffDays == 0)
            {
               document.getElementById('days').value = diffDays + 1;
//               document.getElementById('from_to_time').value = hours_minute;
            }
            else
            {
               document.getElementById('days').value = diffDays;
//               document.getElementById('from_to_time').value = hours_minute;
            }
        }

//    return({"Days":Days,"Hours":Hours,"Minutes":Minutes})
//}

//    var timeResult=SplitTime(hours)
//    console.log("27.3 hours translate to  "+timeResult.Days+"Days "+timeResult.Hours+"Hours and "+timeResult.Minutes+"Minutes.")

//     var date1 = new Date($("#date_start").val());
//     var date2 = new Date($("#date_end").val());
//     var total_hour = date2 - date1
//     var d = moment.duration(total_hour, 'milliseconds');
//     var hour = Math.floor(d.asHours());
//     var minute = Math.floor(d.asMinutes()) - hour * 60;
//     console.log("================================", +timeResult.Days+"Days "+timeResult.Hours+"Hours and "+timeResult.Minutes+"Minutes.))
//     if (Math.floor(d.asDays() == 0){
//        document.getElementById('from_to_time').value = hour+":"+minute ;
//        }
//    else{
//        document.getElementById('from_to_time').value = hour+":"+minute ;
//        }
    });

    $('#button_cancel').click(function(){
            $('input[type="text"]').val(0);
            $('select[id="employee_id"]').empty();
            $('select[id="project_task"]').empty();
    });

    $('#project_task').change(function(){
    console.log("===================vvvvvvvvv========================",document.getElementById('project_task').value)
    if (document.getElementById('project_task').value != 'none'){
    $('input[id="new_task"]').val("");
     $('input[id="new_task"]').prop("disabled",true).addClass("disabled");
     }
     else{
     $('input[id="new_task"]').prop("disabled",false).removeClass("disabled");
     }
     });

       $('#new_task').change(function(){
    console.log("===================vvvvvvvvv========================",document.getElementById('new_task').value)
    if (document.getElementById('new_task').value != ''){
     $('select[id="project_task"]').prop("disabled",true).addClass("disabled");
     $('select[id="project_task"]').prop("required",false).removeClass("required");
     }
     else{
     $('select[id="project_task"]').prop("disabled",false).removeClass("disabled");
     }
//            $('select[id="employee_id"]').empty();
    });
     $('#button_submit').click(function(){
     console.log("===========================================",$("#project_task").val())
     console.log("===========================================",$("#new_task").val())
     console.log("====================================#present_absent",$("#present_absent").val())
            if ( $("#days").val()[0] == '-') {
               alert("Checkout time should be greater then checkin time");
               event.preventDefault();
          }

          if ( $("#employee_id").val() == null || $("#employee_id").val() == 'none') {
               alert("Please select employee");
               event.preventDefault();
          }
          if (($("#project_task").val() == 'none' || $("#project_task").val() == null) && $("#new_task").val() == '')  {
               alert("Please Select Exiting Task Or Enter New task.");
               event.preventDefault();
          }

          if ($("#present_absent").val() == null || $("#present_absent").val() == 'none')  {
               alert("Please Select Attendance.");
               event.preventDefault();
          }
    });

});
});