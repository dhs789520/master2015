<script type="text/javascript" src="/static/question.js"></script>
<script type="text/javascript" src="./static/bootstrap/js/bootstrap.js"></script>
<script>

$("td").click(function(){

    if($("#answer"+this.id).attr('type') == 'checkbox'){
        return ;
    };
    
    $("td").unbind('click');
    $("#answer"+this.id).attr('checked',"checked");
    $("#A").css("background-color",$("#question").css("background-color"));
    $("#B").css("background-color",$("#question").css("background-color"));
    $("#C").css("background-color",$("#question").css("background-color"));
    $("#D").css("background-color",$("#question").css("background-color"));
    $("#E").css("background-color",$("#question").css("background-color"));


    $("#answerA").attr('disabled',"disabled");
    $("#answerB").attr('disabled',"disabled");
    $("#answerC").attr('disabled',"disabled");
    $("#answerD").attr('disabled',"disabled");
    $("#answerE").attr('disabled',"disabled");


    $("#showanswer").attr('disabled',false);

    if (this.id=="{{q.answer}}"){
        $("#"+this.id).css("background-color","#449D44");
        $("#result").html('<font color=blue>√  恭喜你，答案正确!</font>');
    }else{
        $("#"+this.id).css("background-color","red");
        $("#{{q.answer}}").css("background-color","#449D44");
        $("#result").html('<font color=red>X 答案错误</font>');
    };

});


function showAnswer(){
    $("#showanswer").attr('disabled',true);
    var a=""
    if($("#answerA").attr("checked")){ a +="A";};
    if($("#answerB").attr("checked")){ a +="B";};
    if($("#answerC").attr("checked")){ a +="C";};
    if($("#answerD").attr("checked")){ a +="D";};
    if($("#answerE").attr("checked")){ a +="E";};


    $.get("/showAnswer/"+a,function(data,status){
        $("#explain").html(data);
      });

    $("#explain").slideDown();

}


$("#next").click(function(){
  {%if 'next_verify' in user %}
      {%ifequal user.next_verify 2%}
            window.location.href='/next_verify';
      {%endifequal%}
  {%else%}
        window.location.href='/next';
  {%endif%}
});

$("#pre").click(function(){
    window.location.href='/pre';
});


</script>















