"use strict"
var studentCount = 1;

function removeStudent(idStudent){
    studentCount--;
    $(`#navStudent${idStudent}`).remove();
    $(`#student${idStudent}`).remove();
}

function addStudent(){
    studentCount++;
    var htmlTab =
`<li class="nav-item" style="position: relative" id="navStudent${studentCount}">
    <a class="nav-link" id="student${studentCount}-tab" data-toggle="tab" href="#student${studentCount}"
       role="tab" aria-controls="student${studentCount}" aria-selected="false">Student ${studentCount}</a>
       <i class="fa fa-times" style="position: absolute; top: -0.5em; right: 0.1em; font-size: 1.4em; color: orangered; cursor: pointer;"
          onclick="removeStudent(${studentCount})"></i>
</li>`;


    $(htmlTab).insertBefore($(this).parent());

    var htmlStudentForm =
// `<div class="tab-pane fade" id="student${studentCount}" role="tabpanel"
// aria-labelledby="student${studentCount}-tab">
//
// <!--Student Form-->
// <div class="row">
// <div class="form-group col">
// <label for="txtStudent${studentCount}LastName">Last Name
// <span class="text-danger">*</span>
// </label>
// <input type="text" class="form-control"
// id="txtStudent${studentCount}LastName"
// name="txtStudentLastName"
// placeholder="Last Name" required="required"/>
// </div>
// <div class="form-group col">
// <label for="txtStudent${studentCount}MiddleName">Middle Name</label>
// <input type="text" class="form-control"
// id="txtStudent${studentCount}MiddleName"
// name="txtStudentMiddleName"
// placeholder="Middle Name"/>
// </div>
// <div class="form-group col">
// <label for="txtStudent${studentCount}FirstName">First Name
// <span class="text-danger">*</span>
// </label>
// <input type="text" class="form-control"
// id="txtStudent${studentCount}FirstName"
// name="txtStudentFirstName"
// placeholder="First Name" required="required"/>
// </div>
// </div>
//
// <div class="row">
// <div class="form-group col-12">
// <label for="txtStudent${studentCount}Birthday">Birthdate </label>
// <input type="date" class="form-control"
// id="txtStudent${studentCount}Birthday"
// name="txtStudentBirthday"/>
// </div>
// </div>
// <div class = "row">
// <div class="form-group col-6">
// <label for="selStudent${studentCount}GradeLevel">Grade Level of Interest<span
// class="text-danger">*</span></label>
// <select class="custom-select" id="selStudent${studentCount}GradeLevel"
// name="selStudentGradeLevel">
// </select>
// </div>
// <div class="form-group col-6">
// <label for="selStudent${studentCount}SchoolYear">School Year<span
// class="text-danger">*</span></label>
// <select class="custom-select" id="selStudent${studentCount}SchoolYear"
// name="selStudentSchoolYear">
// </select>
// </div>
// <div class="form-group col-6">
// <label for="txtStudent${studentCount}CurrentSchool">Current School</label>
// <input type="text" class="form-control"
// id="txtStudent${studentCount}CurrentSchool"
// name="txtStudentCurrentSchool"
// placeholder="Current School"/>
// </div>
// </div>
//
// </div>`;

    // $(`#selStudent${studentCount}GradeLevel`)
    // Add to new students
// $('#studentsTabContent').append(htmlStudentForm);
    $('#studentsCount').val(studentCount);

    var studentClonnable  = document.getElementById("student1").cloneNode(true);
    var studentTabContent = document.getElementById("studentsTabContent");
    
    studentTabContent.appendChild(studentClonnable);
    
    // Reassign ids
    $(studentClonnable).attr("id", "student"+studentCount);
    $(studentClonnable).attr("aria-labelledby", "student"+studentCount+"-tab");
    $(studentClonnable).removeClass("active");
    $(studentClonnable).removeClass("show");
    
    // Year List
    var optionsSchoolYear = $('select#selStudent1SchoolYear option').clone();
    $('#selStudent'+studentCount+'SchoolYear').append(optionsSchoolYear);

    // Grade Level List
    var optionsGradeLevel = $('select#selStudent1GradeLevel option').clone();
    $('#selStudent'+studentCount+'GradeLevel').append(optionsGradeLevel);
}

function getStates(){
    $('#selState').html("<option value='-1'>-Select a state-</option>");
    $.ajax({
        url: '/admission/states',
        type: 'GET',
        data: { 'country_id': $('#selCountry').val()},
        success: function(data){
            $.each(JSON.parse(data), function(i, state){
                // console.log(`<option
				// value='${state.id}'>${state.name}</option>`);
                $('#selState').append(`<option value='${state.id}'>${state.name}</option>`)
            })
        },
        error: function(){
            console.error("Un error ha ocurrido al cargar los states");
        }
    });

}

$(function(){
    $('#add-tab').on('click', addStudent);
    $('#selCountry').on('change', getStates);
    
    $('.custom-file-input').on("change", function(){
    	var fileName = $(this)[0].files[0].name;
    	$(this).next("label").text(fileName);
    });
    
//    document.querySelector('.custom-file-input').addEventListener('change',function(e){
//    	var fileName = document.getElementById("myInput").files[0].name;
//    	var nextSibling = e.target.nextElementSibling;
//    	nextSibling.innerText = fileName;
//	});
    
// populateStates("txtCountry", "txtState");
});
