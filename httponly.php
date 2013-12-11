<?php
ini_set('session.cookie_httponly', true);
session_start();
?>
<html>
<body>
	<div>Current session_id: <?=session_id()?></div>
	<div>Try to refresh;-)</div>
	<script>
		function printCookies(cookies, title) {
			var cookieElem = document.createElement('div');
			cookieElem.textContent = title + ' cookies: ' + (cookies || 'Empty');
			document.body.appendChild(cookieElem);	
		}
		printCookies(document.cookie, 'Current');
		document.cookie = '<?=session_name()?>[]=any; path=/; expires=1 Jan 2038 00:00:00 GMT';
		printCookies(document.cookie, 'Modified');
	</script>
</body>
</html>

