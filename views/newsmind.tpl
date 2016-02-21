<!DOCTYPE html>
<html lang="zh-CN">

<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->

  <link rel="icon" href="/static/icon.ico">
  <title>新闻挖掘</title>

  <!-- Bootstrap core CSS -->
  <link href="/static/css/bootstrap.min.css" rel="stylesheet">
  <!-- Bootstrap theme -->
  <link href="/static/css/bootstrap-theme.min.css" rel="stylesheet">
  <!-- Custom styles for this template -->
  <link href="/static/css/jumbotron-narrow.css" rel="stylesheet">
</head>

<body role="document">

  <div class="container " role="main">

    <nav class="navbar navbar-inverse">
      <h1 class="navbar-text">网络数据挖掘与分析</h1>
    </nav>

    <div class="jumbotron">
      <p>这是《网络数据挖掘与分析》课程的一个小样，它会收集最近一段时间内的网络新闻数据，并通过重要度分析提取新闻中的关键词，以便学生进一步挖掘最近的新闻热点。</p>
    </div>

    <!-- Button trigger modal -->
    <button type="button" class="btn btn-success" data-toggle="modal" data-target="#newTaskModal" onclick="initModal()">
      新建任务
    </button>
    <p></p>

    <!-- Modal -->
    <div class="modal fade" id="newTaskModal" tabindex="-1" role="dialog" aria-labelledby="newTaskModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h4 class="modal-title" id="newTaskModalLabel">新建任务</h4>
          </div>
          <div class="modal-body">
            <form class="form-horizontal" onsubmit="return checkTaskname()" action="/tasks" method="post" accept-charset="utf-8">
              <div class="form-group" id="tasknameinputdiv">
                <label class="col-sm-2 control-label">任务名称</label>
                <div class="col-sm-10">
                  <input type="text" class="form-control" id="tasknameinput" name="taskname" placeholder="请为新任务命名">
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-2 control-label">新闻频道</label>
                <div class="col-sm-10">
                  <select class="form-control" id="channelselect" name="channelid">
                    % for channel in channels:
                    <option value="{{channel.Id}}">{{channel.name}}</option>
                    % end
                  </select>
                </div>
              </div>
              <div class="form-group">
                <div class="col-sm-offset-2 col-sm-10">
                  <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
                  <button type="submit" class="btn btn-success">提交</button>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer"></div>
        </div>
      </div>
    </div>

    <div class="panel panel-success">
      <!-- panel contents -->
      <div class="panel-heading">任务列表</div>
      <div class="panel-body">
        <p font-color="gray">
          <i>任务列表按照创建时间的先后逆序排列，最新创建的任务排在第一位，点击任务条目可查看任务详情。</i>
        </p>
      </div>

      <!-- List group -->
      <ul class="list-group">
        % for task in tasks:
        <a href="tasks/{{task.name}}" class="list-group-item">
          <h4 class="list-group-item-heading">{{task.name}}</h4>
          <p class="list-group-item-text"><small>创建于: {{task.datestr}}</small></p>
        </a>
        % end
      </ul>
    </div>

  </div>
  <!-- /container -->

  <script>
    function checkTaskname() {
      var taskname = document.getElementById('tasknameinput').value;
      document.getElementById('tasknameinput').value = encodeURI(taskname);
      if (taskname == "" || taskname == null) {
        var inputdiv = document.getElementById('tasknameinputdiv');
        inputdiv.className = inputdiv.className + ' has-error';
        return false;
      }
      else {
        return true;
      }
    }

    function initModal() {
      document.getElementById('tasknameinput').value = "";
      document.getElementById('tasknameinputdiv').className = "form-group";
    }
  </script>
  <!-- Bootstrap core JavaScript -->
  <!-- Placed at the end of the document so the pages load faster -->
  <script src="/static/js/jquery.min.js"></script>
  <script src="/static/js/bootstrap.min.js"></script>
</body>

</html>
