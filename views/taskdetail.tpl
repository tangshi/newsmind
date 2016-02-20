<!DOCTYPE html>
<html lang="zh-CN">

<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->

  <link rel="icon" href="/static/icon.ico">
  <title>任务详情</title>

  <!-- Bootstrap core CSS -->
  <link href="/static/css/bootstrap.min.css" rel="stylesheet">
  <!-- Bootstrap theme -->
  <link href="/static/css/bootstrap-theme.min.css" rel="stylesheet">
  <!-- Custom styles for this template -->
  <link href="/static/css/jumbotron-narrow.css" rel="stylesheet">
</head>

<body role="document">
  <div class="container " role="main">
    <!-- Modal -->
    <div class="modal fade" id="waitModal" tabindex="-1" role="dialog" aria-labelledby="waitModalLabel" data-backdrop="static" data-keyboard="false">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title" id="waitModalLabel">请耐心等待...</h4>
          </div>
          <div class="modal-body">
            <div class="progress">
              <div class="progress-bar progress-bar-success progress-bar-striped active" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <ol class="breadcrumb">
      <li><a href="/">首页</a></li>
      <li class="active">任务详情</li>
    </ol>

    <div class="well">
      <p><b>任务名称：</b>{{task.name}}</p>
      <p><b>创建日期：</b>{{task.newsdata.startDate.strftime("%Y-%m-%d")}}</p>
      <p><b>最近更新：</b>{{task.newsdata.lastMarkTime.strftime("%Y-%m-%d %H:%M:%S")}}</p>
      <p><b>新闻条目：</b>{{len(task.newsdata.newsItems)}}</p>
      <p><b>总计字数：</b>{{task.newsdata.getWordsNum()}}</p>
    </div>

    <div class="panel">
      <div class="panel-body">
      <button id="refreshBtn" type="button" class="btn btn-sm btn-info pull-left">刷新数据</button>
      <form action="/deltask/{{task.name}}" accept-charset="utf-8">
        <button type="submit" class="btn btn-sm btn-danger pull-right">删除任务</button>
      </form>
      </div>
    </div>

    <ul class="list-group">
      <li class="list-group-item list-group-item-success">
        <span class="badge">权重</span>关键词
      </li>
      % i = 0
      % for word, weight in task.newsdata.keywords:
      % i = i + 1
      <li class="list-group-item">
        <span class="badge">{{int(weight*100)}}</span>{{i}}. {{word}}
      </li>
      % end
    </ul>
  </div>
  <!-- /container -->

  <!-- Bootstrap core JavaScript -->
  <!-- Placed at the end of the document so the pages load faster -->
  <script src="/static/js/jquery.min.js"></script>
  <script src="/static/js/bootstrap.min.js"></script>
  <script>
    jQuery(document).ready(function() {
      $("#refreshBtn").click(function() {
        $(document).on('mousedown', function(Event) {
          Event.preventDefault();
        });
        $('#waitModal').modal('show');
        $.post("/tasks/{{task.name}}",{}, function(data, status) {
          window.location="http://localhost:8000/tasks/{{task.name}}";
        });
      });
    });
  </script>
</body>

</html>
