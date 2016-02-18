<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->

    <link rel="icon" href="/static/icon.ico">
    <title>{{task.name}}</title>

    <!-- Bootstrap core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap theme -->
    <link href="/static/css/bootstrap-theme.min.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="/static/css/jumbotron-narrow.css" rel="stylesheet">

</head>

<body role="document">

    <div class="container " role="main">
        <div class="page-header">
            <h1>{{task.name}}</h1>
        </div>

        <div class="row">
            <div class="col-sm-5">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h3 class="panel-title">任务详情</h3>
                    </div>
                    <div class="panel-body">
                        <p><b>创建时间：</b>{{task.datestr}}</p>
                        <p><b>新闻条目：</b>{{len(task.newsdata.newsItems)}}</p>
                    </div>
                </div>
            </div>
            <!-- /.col-sm-5 -->

            <div class="col-sm-7">
                <div class="panel panel-success">
                    <div class="panel-heading">
                        <h3 class="panel-title">关键词排行榜</h3>
                    </div>
                    <div class="panel-body">
                        <ol>
                            % for word, weight in task.newsdata.getKeyWords(10):
                            <li>{{word}} : {{weight}}</li>
                            % end
                        </ol>
                    </div>
                </div>
            </div>
            <!-- /.col-sm-7 -->
        </div>
    </div>
    <!-- /container -->

    <!-- Bootstrap core JavaScript -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
</body>

</html>
