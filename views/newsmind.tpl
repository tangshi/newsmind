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

        <div>
            <p>
                <a href="newtask" class="btn btn-success active" role="button">新建任务</a>
            </p>

            <div class="panel panel-success">
                <!-- panel contents -->
                <div class="panel-heading">任务列表</div>
                <div class="panel-body">
                    <p>
                        <i>任务列表按照创建时间的先后逆序排列，最新创建的任务排在第一位，点击任务条目可查看任务详情。</i>
                    </p>
                </div>

                <!-- List group -->
                <ul class="list-group">
                    % for name in tasknames:
                    <a href="tasks/{{name}}" class="list-group-item">
                        <h4>{{name}}</h4>
                    </a>
                    % end
                </ul>
            </div>
        </div>


    </div> <!-- /container -->

    <!-- Bootstrap core JavaScript -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
</body>

</html>
