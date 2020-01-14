
function myclick(char_length) {
    var numArr = new Array();
    var flag;
    var inputs = $("div[id=container] :input");
    console.log(inputs)
    for(var i=0;i<inputs.length;i++){
        var id = inputs[i].id;
        var value = inputs[i].value;
        if (value == '' || value == undefined || value == null||value.length != char_length){
            inputs[i].style.borderColor = "red"; //添加css样式
            inputs[i].
            flag = false
            return
        }else {
            inputs[i].style.borderColor = ""; //取消css样式
        }
        numArr.push({id:id,value:value});//添加至数组
    }

//     $('input').each(function(){
//        var id1 = $(this).attr("id");
//        var v = $(this).val();
//       if (v == '' || v == undefined || v == null||v.length != char_length){
//            $(this).css('borderColor','red'); //添加css样式
//            flag = false
//            return
//        }else {
//            $(this).css('borderColor',''); //取消css样式
//        }
//        numArr.push({id:id1,value:v});//添加至数组
//    });
    console.log(numArr);
    if(flag==false){
        alert("输入不合法！")
        return
    }
    $.ajax({
        url:"/submit",
        type:"post",
        data:JSON.stringify(numArr),
        success:function(flag){
                    alert(flag)
        }
    })
    console.log("button返回修改被点击了")
}
