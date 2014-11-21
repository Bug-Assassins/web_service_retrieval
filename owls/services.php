<!DOCTYPE HTML>
<html>
<head>
<style type="text/css">
	
	table td,th{
		width:150px;
		height: 30px;
		text-align:center;
	}

	#services {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    width: 100%;
    border-collapse: collapse;
	}

	#services td, #services th {
    font-size: 1em;
    border: 1px solid #98bf21;
    padding: 3px 7px 2px 7px;
	}

	#services th {
    font-size: 1.1em;
    padding-top: 5px;
    padding-bottom: 4px;
    background-color: #A7C942;
    color: #ffffff;
	}

	#services tr.alt td {
    color: #000000;
    background-color: #EAF2D3;
	}	

</style>
</head>
<body>

<?php
	
	session_start();
	if(isset($_POST['sub']))
	{
        if (!isset($_POST["input"]) || trim($_POST["input"]) == "")
        {
        	echo "here";
            header('Location:search.php?error=3');
        }
        else if (!isset($_POST["output"]) || trim($_POST["output"]) == "")
        {
            header('Location:search.php?error=4');
        }
        else if (!isset($_POST["theta"]))
        {
            header('Location:search.php?error=5');
        }
        else if (!is_numeric($_POST["theta"]))
        {
            header('Location:search.php?error=6');
        }
        
		$in = '"'.$_POST["input"].'"';
		$out = '"'.$_POST["output"].'"';
		$theta = $_POST["theta"];
		if(!($theta >= 0 && $theta <=1))
		{
			header('Location:search.php?error=7');	
		}
        if ($theta == "")
        $theta = 0.5;
        
	}
	else
	{
		$in = '"'.$_SESSION["inp"].'"';
		$out = '"'.$_SESSION["out"].'"';
		$theta = '"'.$_SESSION["theta"].'"';
	}
	$shell = "bash main.sh";
	$cmd = $shell." ".$in." ".$out." ".$theta;
	$output = shell_exec($cmd);
	$file = fopen("result.temp","r");
?>
	
	<table id='services'>
		<tr>
			<th>Name of Service</th>
			<th>Input Score</th>
			<th>Output Score</th>
			<th>Average</th>
		</tr>

<?php
	$flag = false;
	while(!feof($file))
	{
		
		$line = fgets($file);
		if($line === false)
			break;
		$token = strtok($line, ":");
		$i = 0;
		if($flag === false)
			echo "<tr>";
		else
			echo "<tr class='alt'>";
		while ($token !== false)
		{
			$arr[ $i++ ] = $token;
			$token = strtok(":");
		}

		echo "<td><a href='docs/$arr[0]'>$arr[0]</a></td>";
		echo "<td>$arr[2]</td>";
		echo "<td>$arr[3]</td>";
		echo "<td>$arr[1]</td></tr>";
		$flag = !($flag);
	}	

	fclose($file);
?>
	</table>
</body>
</html>