entry_page = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>입장 확인</title>
<style>
  body { display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; }
  h2 { font-size: 2.5em; }
</style>
</head>
<body>
  <div>
    <h2>입장하시겠습니까?</h2>
    <form method="POST">
      <button type="submit" style="font-size: 1.5em; padding: 0.5em 1em;">입장</button>
    </form>
  </div>
</body>
</html>
"""

confirmed_page = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>입장 완료</title>
<script>
  history.pushState(null, "", location.href);
  window.onpopstate = function () { history.go(1); };
</script>
<style>
  body { display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; }
  h2 { font-size: 2.5em; }
</style>
</head>
<body>
  <h2>✅ 확인되었습니다.</h2>
</body>
</html>
"""

already_page = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>중복 입장</title>
<style>
  body { display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; }
  h2 { font-size: 2.3em; color: red; }
</style>
</head>
<body>
  <h2>❌ 이미 입장하셨습니다.</h2>
</body>
</html>
"""
