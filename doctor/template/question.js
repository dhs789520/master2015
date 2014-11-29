<script type="text/javascript" src="/static/question.js"></script>
<script type="text/javascript" src="/static/jquery.js"></script>
<script type="text/javascript" src="/static/bootstrap/js/jquery.js"></script>
<script type="text/javascript" src="/static/bootstrap/js/bootstrap.js"></script>
<script>

//选项被击中，显示状态
$("td").click(function(){

    //多项选择题被选中后，直接返回
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


//点击上一题按钮
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


//点击下一题按钮
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



$('.star_icon').unbind("click");
$('.star_icon').click(function () {

    if (!$(this).hasClass("favorite")) {//增加收藏
     $.get("/store_question/{{q.id}}",function(data,status){
         if(data=='success'){
            $("#qstore").toggleClass("favorite");
            $("#qstore_info").html("已收藏");
            
         }; //endif
      }); //endof get 


    }
    else if ($(this).hasClass("favorite")) { //取消收藏功能函数
     $.get("/store_question/-{{q.id}}",function(data,status){
         if(data=='success'){
                $("#qstore").toggleClass("favorite");
                $("#qstore_info").html("点亮星收藏");
             };//endif
        });//endof get
    };// endof elseif

});




//设置题型按钮内容
if(1=={{q.qtype}}){
    $("#qtype").html('单项选择题');
}else if(2=={{q.qtype}}){
    $("#qtype").html('多项选择题');
}else if(3=={{q.qtype}}){
    $("#qtype").html('共用题干题共用备选答案题');
}else if(4=={{q.qtype}}){
    $("#qtype").html('共用备选答案题');
}



</script>















