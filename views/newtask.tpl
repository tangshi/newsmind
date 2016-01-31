<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->

    <link rel="icon" href="/static/icon.ico">
    <title>新建任务</title>

    <!-- Bootstrap core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap theme -->
    <link href="/static/css/bootstrap-theme.min.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="/static/css/jumbotron-narrow.css" rel="stylesheet">

</head>

<body role="document">

    <div class="container " role="main">
        <form class="form-horizontal" onsubmit="return checkTaskname()" action="/newtask" method="post">
            <div class="form-group" id="tasknameinputdiv" >
                <label class="col-sm-2 control-label">任务名称</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="tasknameinput" name="taskname" placeholder="请为新任务命名">
                </div>
            </div>
            <div class="form-group">
                <label class="col-sm-2 control-label">新闻频道</label>
                <div class="col-sm-10">
                    <select class="form-control" id="channelnameselect" name="channelname">
                        % for channel in channels:
                        <option>{{channel.name}}</option>
                        % end
                    </select>
                </div>
            </div>
            <div class="form-group">
                <div class="col-sm-offset-2 col-sm-10">
                    <button type="submit" class="btn btn-success">提交</button>
                </div>
            </div>
        </form>

    </div>
    <!-- /container -->

    <script>
        function checkTaskname() {
            var taskname = document.getElementById('tasknameinput').value;
            if (taskname == "" || taskname == null) {
                var inputdiv = document.getElementById('tasknameinputdiv');
                inputdiv.className = inputdiv.className + ' has-error';
                return false;
            }
            else {
                return true;
            }
        }
    </script>
    <!-- Bootstrap core JavaScript -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
</body>

</html>
