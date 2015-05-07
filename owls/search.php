<html>
<head><title>Web Service Search</title>
<style>
.search {
    margin-left:auto;
    margin-right:auto;
    max-width: 500px;
    background: #F2F2F2;
    padding: 30px 30px 20px 30px;
    box-shadow: rgba(187, 187, 187, 1) 0 0px 20px -1px;
    -webkit-box-shadow: rgba(187, 187, 187, 1) 0 0px 20px -1px;
    font: 16px Georgia, "Times New Roman", Times, serif;
    font-weight:bold;
    color: #666;
    border-radius: 10px;
    -webkit-border-radius: 10px;
}
.search h3 {
    font: 24px "Trebuchet MS", Arial, Helvetica, sans-serif;
    padding: 20px 0px 20px 40px;
    display: block;
    margin: -30px -30px 10px -30px;
    color: #FFF;
    background: #9DC45F;
    text-shadow: 1px 1px 1px #949494;
    border-radius: 5px 5px 0px 0px;
    -webkit-border-radius: 5px 5px 0px 0px;
    -moz-border-radius: 5px 5px 0px 0px;
    border-bottom:1px solid #89AF4C;

}
.search h3>span {
    display: block;
    font-size: 11px;
    color: #FFF;
}
.search label {
    display: block;
    margin: 0px 0px 5px;
}
.search label>span {
    float: left;
    width: 20%;
    text-align: right;
    padding-right: 10px;
    margin-top: 10px;
    color: #969696;
}
.search input[type="text"]{
    color: #555;
    width: 70%;
    padding: 3px 0px 3px 5px;
    margin-top: 2px;
    margin-right: 6px;
    margin-bottom: 16px;
    border: 1px solid #e5e5e5;
    background: #fbfbfb;
    height: 25px;
    line-height:15px;
    outline: 0;
    -webkit-box-shadow: inset 1px 1px 2px rgba(200,200,200,0.2);
    box-shadow: inset 1px 1px 2px rgba(200,200,200,0.2);
}

.search .button {
    background-color: #9DC45F;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-border-radius: 5px;
    border: none;
    padding: 10px 25px 10px 25px;
    color: #FFF;
    text-shadow: 1px 1px 1px #949494;
}
.search .button:hover {
    background-color:#80A24A;
}

</style>
</head>
<body>
<div >
<?php
if (isset($_REQUEST['error']))
{
?>
<?php
	switch($_REQUEST['error'])
	{
		case '1' :
?>	
<h3 style="color:red;">File size too big</h3>
<?php
			break;
		case '2' :
?>	
<h3 style="color:red;">Not a OWLS document</h3>
<?php
			break;
		case '3' :
?>
<h3 style="color:red;">Input field is empty</h3>
<?php
			break;
		case '4' :
?>
<h3 style="color:red;">Output field is empty</h3>
<?php
			break;
		case '5' :
?>
<h3 style="color:red;">Cutoff not set</h3>
<?php
			break;
		case '6' :
?>
<h3 style="color:red;">Cutoff is not numeric</h3>
<?php
			break;
		case '7' :
?>
<h3 style="color:red;">Cutoff not within limits</h3>
<?php
			break;
	}
}
?>
<script>
	function validate()
	{
		var x, y, z;
		x = document.forms["search"]["input"].value;
		y = document.forms["search"]["output"].value;
		z = document.forms["search"]["theta"].value;
		if (x == "" || y == "")
		{
			alert("Empty");
			return false;
		}
		if (z == "")
		{
			document.forms["search"]["theta"].value = 0.5;
			return true;
		}
		if (isNaN(z))
		{
			alert("Cutoff should be a number");
			return false;
		}
		z = +z;
		if (!( z >= 0 && z<= 1))
		{
			alert("Cutoff should be between 0 and 1");
		}
		return true;
	}
</script>

<form  name="search" class="search" method="POST" onsubmit="return validate();" action="services.php">

<h3>Search Web Services
        <span>Please fill in the fields to search.</span>
</h3><br/>
<label>
    <span>Input</span>
    <input type="text" name="input" id="input"/>
</label>
<label>
    <span>Output</span>
    <input type="text" name="output" id="output"/>
</label>
<!--<label>
    <span>Cutoff</span>
    <input type="text" name="theta" id="theta"/>
</label>-->
<label>
    <input type="checkbox" name="composite" value="1">
    <span>Composite</span>
</label>
<label>
    <span>&nbsp;</span>
    <input type="submit" class="button" name="sub" value="Submit"/>
</label>

</form>
<br/>
<form action="upload.php" class="search" method="POST" enctype="multipart/form-data">
  <h3>Upload OWL file</h3> <br/>
  <label><input type="file" name="owl" id="owl"></label><br/>
  <label><input type="submit" class="button" name="submit"></label>
</form>
</div>
</body>
</html>
