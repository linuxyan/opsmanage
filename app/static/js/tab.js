
//获取当前时间
function current(){
    var d = new Date(),
        str = "";
    var weekday=new Array(7);
    weekday[0]="星期天";
    weekday[1]="星期一";
    weekday[2]="星期二";
    weekday[3]="星期三";
    weekday[4]="星期四";
    weekday[5]="星期五";
    weekday[6]="星期六";
    str+=d.getFullYear()+'年';
    str+=d.getMonth()+1+'月';
    str+=d.getDate()+'日'+'&nbsp;';
    str+=d.getHours()+':';
    str+=d.getMinutes()+':';
    str+=d.getSeconds()+'&nbsp;';
    str+=weekday[d.getDay()];
    return str;
}
setInterval(
    function(){
        $("#nowTime").html(current)},1000
    );
//获取当前时间

$(function(){
    $(".vtitle span").click(function(){
		var leftparent=$(this).parent();
		var leftul=$(this).parent().find("ul");
        leftul.slideToggle();
        leftparent.addClass("active").siblings().removeClass("active");

		var showul=leftul.css("display")==="block";
		if(showul==true){
		    	leftparent.find('i').addClass('roowbg-right')
		}
		
    })
    $(".vtitle ul li").each(function(){
        $(this).click(function(){
            $(this).parent().find(".vconlist").css("display","block");
        })
    })
    $(".user").toggle(
        function(){
            $(this).click(function(){
                $(".change").show();
            })
        },function(){
            $(this).click(function(){
                $(".change").hide();
            })
        }
    )






 //授权页面追加js   
 $(function(){
            //移到右边
    $('#add').click(function(){
        //获取选中的选项，删除并追加给对方
        $('#select1 option:selected').appendTo('#select2');
    });

    //移到左边
    $('#remove').click(function(){
        $('#select2 option:selected').appendTo('#select1');
    });

    //全部移到右边
    $('#add_all').click(function(){
        //获取全部的选项,删除并追加给对方
        $('#select1 option').appendTo('#select2');
    });

    //全部移到左边
    $('#remove_all').click(function(){
        $('#select2 option').appendTo('#select1');
    });

    //双击选项
    $('#select1').dblclick(function(){ //绑定双击事件
        //获取全部的选项,删除并追加给对方
        $("option:selected",this).appendTo('#select2'); //追加给对方
    });

    //双击选项
    $('#select2').dblclick(function(){
        $("option:selected",this).appendTo('#select1');
    });
    })
     //授权页面追加js

    //项目授权提交
    $('#submit_user_pro').click(function(){
	    var array = new Array();
        $("#select2 option").each(function(){
            var txt = $(this).text();
            array.push(txt);
         });
        //alert(array.join());
        $.ajax({
            type : 'post',
            url: "",
            dataType:'text',
            data : {
                    'pro_list' :  array.join()
            },
            success: function(data){
                layer.alert(data, {icon: 1});
                $(".layui-layer-btn0").click(function(){
                    location.reload();
                })
            }
        });
	});
    //项目授权提交
    
    //数据库授权提交
    $('#submit_user_db').click(function(){
	    var array = new Array();
        $("#select2 option").each(function(){
            var txt = $(this).val();
            array.push(txt);
         });
        //alert(array.join());
        $.ajax({
            type : 'post',
            url: "",
            dataType:'text',
            data : {
                    'db_list' :  array.join()
            },
            success: function(data){
                layer.alert(data, {icon: 1});
                $(".layui-layer-btn0").click(function(){
                    location.reload();
                })
            }
        });
	});
    //数据库授权提交

    //input里面内容获取file地址
    var $fileField = $("#fileField");
        $key = $("#key");
        $fileField.on("change",function(){
            var that =$(this);
            $key.val(that.val());
        })
    //input里面内容获取file地址

    //项目管理页面删除模态框
    var $prode1=$('.prode1').find('font');
    var $prode2=$('.prode2').find('font');
    var $prode3=$('.prode3').find('font');
    var $proId=$('#proId');
    $(".del").click(function(){
         $(".productdel").css("display","block");
        var that = $(this);

        var proid=that.attr('pro-id');

        var proname=that.attr('pro-name');
        // alert(proname);
        var hostip=that.attr('host-ip');
        // alert(hostip);
        var prodomain=that.attr('pro-domain');
        // alert(prodomain);
        $proId.val(proid);
        $prode1.html(proname);
        $prode2.html(hostip);
        $prode3.html(prodomain);

    });

    $('.suredel').on('click',function(){
        // alert($proId.val());
        $.ajax({
            type : 'post',
            url: "",
            // dataType:'text',
            data : {
                        'product_id' : $proId.val(),
                        'operation' :  'delete_product'
                    },
            success:function(data){
                            layer.alert(data, {icon: 1});
                            $(".layui-layer-btn0").click(function(){
                                location.reload();
                            })
                    }
            })
    })





    //项目管理页面删除模态框
    //更新弹出框 
        var $NewId=$("#NewId");
        $(".new").click(function(){
            var $pronewId=$(this).parents().find('.pro-id');
            $NewId =$pronewId.html();
            // alert($NewId)
            // alert($pronewId.html());
            $.ajax({
                type:'post',
                url:"",
                data:{
                    'product_id' : $pronewId.html(),
                    'operation' :  'get_curversion'
                },
                success: function(data){
                        $(".newload").css("display","block")
                        var obj = JSON.parse(data);
                        var cur = obj.cur_version;
                        var old = obj.old_version;
                        // alert(cur);
                        // alert(old);
                        // var $New = $(".newload");
                        var $current = $(".newload .current span");
                        var $onone = $(".newload .Onone span");
                        // alert($onone.html());
                        var $Opts = $(".newload .current font");
                        $Opts.html(cur).html();
                        var $Opt = $(".newload .Onone font");
                        $Opt.html(old).html();
                        // alert($Old);
                    }
            })
        });
        
        $(".close").click(function(){
            $(".newload").hide();
        })
        $(".cancel").click(function(){
            $(".newload").hide();
        })

        
        $(".news").click(function(){
            // var $productid = $(this).parents().find(".liucheng").children().find(".pro-id");
            var $version = $("#up_version").val();
            var index = layer.load(1, {
                shade: [0.1,'#fff'] ,
                time: 3300,
            });
            // alert($NewId)
            $.ajax({
                    type:'post',
                    url:"",
                    data:{
                        'product_id' : $NewId,
                        'operation' :  'update',
                        'version': $version
                    },
                    success:function(data){

                        
                        $(".newload").hide();
                        $(".modol1").css("display","block");
                        var $visions = $(".visions li");
                        $visions.html(data);


                       // alert(aaa);
                        // alert(data);

                        }
                    })
            })
           
                // $(".modol1").css("display","block");
            
            $(".cancel").click(function(){
                $(".modol1").hide();
            })
            $(".modol1 .close").click(function(){
                $(".modol1").hide();
            })
    $(".new1").click(function(){
        $(".modol1").hide();
    })

    //更新弹出框

    //项目管理页关闭按钮
    $("#stop a").click(function(){
        var $productId = $(this).parents().find(".pro-id");
        var index = layer.load(1, {
                shade: [0.1,'#fff'] ,
                time: 3300,
            });
        // alert($productId.html());
        $.ajax({
            type:'post',
            url:"",
            data:{
                'product_id' : $productId.html(),
                'operation' :  'stop'
            },
            success:function(data){
                layer.alert(data, {icon: 1});
            }
        })
    })
    //项目管理页关闭按钮

    //项目管理页启动按钮
    $("#start a").click(function(){
        var $productId = $(this).parents().find(".pro-id");
        var index = layer.load(1, {
                shade: [0.1,'#fff'] ,
                time: 3300,
            });
        $.ajax({
            type:'post',
            url:"",
            data:{
                'product_id' : $productId.html(),
                'operation' :  'start'
            },
            success:function(data){
                layer.alert(data, {icon: 1});
            }
        })
    })
    //项目管理页启动按钮

    //项目管理页重启按钮
    $("#restart a").click(function(){
        var $productId = $(this).parents().find(".pro-id");
        var index = layer.load(1, {
                shade: [0.1,'#fff'] ,
                time: 3300,
            });
        $.ajax({
            type:'post',
            url:"",
            data:{
                'product_id' : $productId.html(),
                'operation' :  'restart'
            },
            success:function(data){
                layer.alert(data, {icon: 1});
            }
        })
    })
    //项目管理页重启按钮

    //判断上传文件是否为sql
    function check(){
        var filepath=path.value
        filepath=filepath.substring(filepath.lastIndexOf('.')+1,filepath.length)
            if(filepath != 'sql')
            alert("只能上传sql类型的文件")
        }
    //判断上传文件是否为sql


    //取服务器管理页面删除的数据
        var $server_Name=$(".de1").find('font');
        var $server_ip=$(".de2").find('font');
        var $currentId = $('#currentId');
        var $valideBtn = $('.valide-btn'),
            $deleteBtn = $('.deleteBtn');
        $deleteBtn.click(function(){
            var that = $(this);
            var hostId = that.attr('host-id');

            // var $serverId = that.attr('host-id');
            //     alert($serverId);
            var $serverName = that.attr('host-hostname');
                // alert($serverName);
            var $hostIp = that.attr("host-hostip");
                // alert($hostIp);
            $currentId.val(hostId);    
            $server_Name.html($serverName);
            $server_ip.html($hostIp);

           
            $(".modols").css("display","block");
        })
        $(".close").click(function(){
            $(".modols").hide();
        })
        $(".cancel").click(function(){
            $(".modols").hide();
        })
       

        $(".sure").on("click",function(){
            $(".modols").hide();
           // alert($currentId.val());
                 $.ajax({
                    type : 'post',
                    url: "",
                    dataType:'text',
                    data : {
                            'server_id' :  $currentId.val(),
                            'operation' :  'delete_server'
                    },
                    success: function(data){
                            
                            layer.alert(data, {icon: 1});
                            $(".layui-layer-btn0").click(function(){
                                location.reload();
                            })
                            
                        }

                });
           }); 

    //取服务器管理页面删除的数据

   

    //用户管理页面删除弹出框
    var $Username = $(".username").find('font');
    // alert($Username.html());
    var $Name = $('.name').find('font');
    var $usernameId=$("#userId");
    $('.userdel').click(function(){
        var that = $(this);
        var $userUsername = that.attr("user-username");
        var $userName = that.attr("user-name");
        var $userId = that.attr("user-id");
        
        // alert($userId);
        // alert($userUsername);
        $('.usermodol').show();
        $Username.html($userUsername);
        $Name.html($userName);
        $usernameId.val($userId);
        
        // alert(($usernameId.val($userId)).html());
    });
    $(".usersure").click(function(){
        // alert($usernameId.val());
        $.ajax({
            type:'post',
            url:'',
            dataType:'text',
            data:{
                'user_id' :  $usernameId.val(),
                'operation' :  'del_user'
            },
            success:function(data){
                layer.alert(data, {icon: 1});
                 $(".layui-layer-btn0").click(function(){
                    location.reload();
                })
            }
        })
    });


    //用户管理页面删除弹出框

    //服务器管理验证按钮
    $valideBtn.click(function(){
        var that =$(this);
        var $hostid = that.attr("host-id");
        var index = layer.load(1, {
                shade: [0.1,'#fff'] ,
                time: 3300,
            });
			
        // alert($hostid);
        $.ajax({
            type: 'post',
            url: "",
            dataType: 'text',
            data: {
                'server_id': $hostid,
                'operation': 'test_server'
            },
			beforeSend: function () {
				$("loading").show();
			},
                success: function(data) {
                    layer.closeAll('loading');
                    // alert(data);
                    layer.alert(data, {icon: 6});
					that.attr({"disabled":true})
                }

            })
    });
    
 })
 
 
 //添加任务页面
 