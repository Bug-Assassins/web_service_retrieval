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
        //else if (!isset($_POST["theta"]))
        //{
         //   header('Location:search.php?error=5');
        //}
        //else if (!is_numeric($_POST["theta"]))
        //{
        //    header('Location:search.php?error=6');
        //}
        
		$in = '"'.$_POST["input"].'"';
		$out = '"'.$_POST["output"].'"';
		$theta = 0; //$_POST["theta"];
		if(!($theta >= 0 && $theta <=1))
		{
			header('Location:search.php?error=7');	
		}
        if ($theta == "")
        $theta = 0.5;

    	$final_query = $_POST["input"].'#'.$_POST["output"];
        
	}
	else
	{
		$in = '"'.$_SESSION["inp"].'"';
		$out = '"'.$_SESSION["out"].'"';
		$theta = '"'.$_SESSION["theta"].'"';
	}

	//Creating Socket
	if(!($sock = socket_create(AF_INET, SOCK_STREAM, 0)))
	{
	    $errorcode = socket_last_error();
	    $errormsg = socket_strerror($errorcode);

	    die("Couldn't create socket: [$errorcode] $errormsg \n");
	}

	//echo "Socket created";
	$address = '127.0.0.1';
	$port = 12002;
	$composite_port = 12010;

	if(isset($_REQUEST['composite']) && $_REQUEST['composite'] == "1")
	{
		$port = $composite_port;
	}

	if(!socket_connect($sock , $address , $port))
	{
	    $errorcode = socket_last_error();
	    $errormsg = socket_strerror($errorcode);

	    die("Could not connect: [$errorcode] $errormsg \n");
	}

	//Sending Query
	if( ! socket_send ( $sock , $final_query, strlen($final_query) , 0))
    {
        $errorcode = socket_last_error();
        $errormsg = socket_strerror($errorcode);
        socket_close($sock);
        die("Could not send data: [$errorcode] $errormsg \n");
    }

    $res = null;

    if( ! socket_recv( $sock, $res, 500000, 0) )
	{
		$errorcode = socket_last_error();
        $errormsg = socket_strerror($errorcode);
        socket_close($sock);
        die("Could not send data: [$errorcode] $errormsg \n");
	}

	//echo $res;

	if(isset($_REQUEST['composite']) && $_REQUEST['composite'] == "1")
	{
		$out = explode('|', $res);
		foreach($out as $val)
		{
			$xx = explode(',', $val);
			echo "<b>Input Score : </b>".$xx[0]."<br/>";
			echo "<b>Output Score : </b>".$xx[1]."<br/>";
			echo "<b>Composition : </b><br/>";
			for ($i = 2; $i < count($xx); $i++)
			{
				echo "<a href='docs/". $xx[$i] ."'>".$xx[$i]."</a> <br/>";
			}
			echo "<br/><br/><br/>";
		}
	}
	else
	{
		?>
		<table id='services'>
			<tr>
				<th>Name of Service</th>
				<!--<th>Input Score</th>
				<th>Output Score</th>
				<th>Average</th> -->
			</tr>

			<?php
				$flag = false;
				$out = strtok($res, ',');
				while($out !== false)
				{
					if($flag === false) echo "<tr>";
					else echo "<tr class='alt'>";
					$flag = !($flag);

					echo "<td><a href='docs/". $out ."'>".$out."</a></td>";
					$out = strtok(',');	
				}
			?>
		</table>
		<?php
	}
	?>
</body>
</html>