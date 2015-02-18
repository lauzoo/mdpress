function saveAs(title, content)
{
	var contentTemplate =	'<!DOCTYPE html>' + 
							'<html lang="zh">' + 
							'<head>' +
							'	<meta charset="utf-8" />' + 
							'	<title>{{{ title }}}</title>' +
							'    <link rel="stylesheet" href="css/style.css" />' + 
						    '    <link rel="stylesheet" href="css/editormd.css" />' +
						    '</head>' +
							'<body>' +
						    '  <div id="content">' +
							'{{{ content }}}' +
							'	</div>' +
							'</body>' ;
	var templateFunction = Handlebars.compile(contentTemplate);
	var data = {"title": title, "content": content};
	var result = templateFunction(data);
	var w = window.open("about:blank", "导出",
			"height=0,width=0,toolbar=no,menubar=no,scrollbars=no,resizable=on,location=no,status=no");
	var dt = new Date();
	
	w.document.charset = "utf8";
	w.document.write(result);

	if (name == null)
	{
		name = dt.getFullYear() + "-" + (dt.getMonth() + 1) + "-" + dt.getDate() + "-" + dt.getTime() + ".html";
	}

	w.document.exeCommand("SaveAs", false, name);
	w.close();
}
