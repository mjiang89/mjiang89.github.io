<html>
	<head>
		<title>Concept-level aspect mining</title>
	</head>
	<body>
<?php include('connect.php'); ?>
	<p><a href="index.php">Back</a>
	<b>Concept-level aspect mining</b></p>
<?php
	$dataset = 'demo';
	if (isset($_REQUEST['dataset'])) {
		$dataset = $_REQUEST['dataset'];
	}
	$level = 'document';
	if (isset($_REQUEST['level'])) {
		$level = $_REQUEST['level'];
	}
	$query = -1;
	if (isset($_REQUEST['query'])) {
		$query = $_REQUEST['query'];
	}
	$aspect = -1;
	if (isset($_REQUEST['aspect'])) {
		$aspect = $_REQUEST['aspect'];
	}
	$claim = -1;
	if (isset($_REQUEST['claim'])) {
		$claim = $_REQUEST['claim'];
	}
	$sentence = '';
?>
<?php
	echo '<p><a name="table1">Table 1</a>: query phrases in the dataset <b>' . $dataset . '</b>. Please select a query phrase:</p>';
	$tablename = $dataset . '_phrase';
	if ($conn = @mysqli_connect($host, $username, $password)) {
		mysqli_select_db($conn, $dbname);
		$result = mysqli_query($conn, 'SELECT phrase_id, phrase, count_dataset, count_claim_document, count_claim_sentence FROM ' . $tablename . ';');
		if (mysqli_num_rows($result) > 0) {
			$html = '<div style="width: 90%;">';
			$html .= '<table style="width: 99%; table-layout:fixed;" border="1">';
			$html .= '<tr>';
			$html .= '<td align="left" style="width: 46%; word-wrap:break-word;"><b>' . 'Phrase' . '</b></td>';
			$html .= '<td align="right" style="width: 18%; word-wrap:break-word;"><b>' . 'Frequency in the dataset' . '</b></td>';
			$html .= '<td align="right" style="width: 18%; word-wrap:break-word;"><b>' . 'Count of document-level claims' . '</b></td>';
			$html .= '<td align="right" style="width: 18%; word-wrap:break-word;"><b>' . 'Count of sentence-level claims' . '</b></td>';
			$html .= '</tr></table></div>';
			$html .= '<div style="overflow: auto; max-height: 200px; width: 90%;">';
			$html .= '<table style="width: 99%; table-layout:fixed;" border="1">';
			while ($row = mysqli_fetch_object($result)) {
				$html .= '<tr ' . ($query == $row->phrase_id ? 'style="background-color:yellow"; id="selected_phrase"' : '') . '>';
				$html .= '<td align="left" style="width: 46%; word-wrap:break-word;"><a href="main.php?dataset=' . $dataset . '&query=' . $row->phrase_id . '&level=' . $level . '#table1">' . $row->phrase . '</a></td>';
				$html .= '<td align="right" style="width: 18%; word-wrap:break-word;">' . number_format($row->count_dataset, 0, '.', ',') . '</td>';
				$html .= '<td align="right" style="width: 18%; word-wrap:break-word;' . ($level == 'document' ? ' color:red;' : '') . '">' . number_format($row->count_claim_document, 0, '.', ',') . '</td>';
				$html .= '<td align="right" style="width: 18%; word-wrap:break-word;' . ($level == 'sentence' ? ' color:red;' : '') . '">' . number_format($row->count_claim_sentence, 0, '.', ',') . '</td>';
				$html .= '</tr>';
			}
			$html .= '</table></div>';
			$html .= '<script>';
			$html .= 'var selected_phrase=document.getElementById("selected_phrase");';
			$html .= 'selected_phrase.scrollIntoView();';
			$html .= '</script>';
			echo $html;
		} else {
			echo 'We cannot find any query phrase in dataset <i>' . $dataset . '</i>.';
		}
		mysqli_close($conn);
	} else {
		echo 'Connection failed.';
	}
?>	
<?php
	echo '<p>Level of phrase embedding (bold for <b>selected</b>): ';
	$is_valid = isset($level) && $level == 'document';
	if ($is_valid) echo '<b>';
	else echo '<a href="main.php?dataset=' . $dataset . ($query < 0 ? '' : '&query=' . $query) . '&level=document">';
	echo 'Document';
	if ($is_valid) echo '</b>';
	else echo '</a>';
	echo ' ';
	$is_valid = isset($level) && $level == 'sentence';
	if ($is_valid) echo '<b>';
	else echo '<a href="main.php?dataset=' . $dataset . ($query < 0 ? '' : '&query=' . $query) . '&level=sentence">';
	echo 'Sentence';
	if ($is_valid) echo '</b>';
	else echo '</a>';
	echo ' | ';
	if ($query < 0) {
		for ($i = 0; $i < 30; $i++) {
			echo '<br />';
		}
		return;
	}
	$tablename = $dataset . '_phrase';
	if ($conn = @mysqli_connect($host, $username, $password)) {
		mysqli_select_db($conn, $dbname);
		$result = mysqli_query($conn, 'SELECT phrase, count_claim_document, count_claim_sentence FROM ' . $tablename . ' WHERE phrase_id = ' . $query . ';');
		if (mysqli_num_rows($result) > 0) {
			$html = 'We find <b style="color:red">';
			while ($row = mysqli_fetch_object($result)) {
				$query_phrase = $row->phrase;
				if ($level == 'document') $html .= number_format($row->count_claim_document, 0, '.', ',');
				if ($level == 'sentence') $html .= number_format($row->count_claim_sentence, 0, '.', ',');
				break;
			}
			$html .= '</b> claims for query <b style="color:red">' . $query_phrase . '</b>';
			echo $html;
		} else {
			echo 'We cannot find claims for query #' . $query . ' <b>' . $query_phrase . '</b>';
		}
		mysqli_close($conn);
	} else {
		echo 'Connection failed.';
	}
	echo '</p>';
?>
<?php
	echo '<p><a name="table2">Table 2</a>: SIMILAR PHRASES with the query <b>' . $query_phrase . '</b> forming a <i>concept</i>.</p>';
	$tablename = $dataset . '_' . $level . '_query';
	if ($conn = @mysqli_connect($host, $username, $password)) {
		mysqli_select_db($conn, $dbname);
		$result = mysqli_query($conn, 'SELECT rank, phrase_id, phrase, score, count_claim, similarity FROM ' . $tablename . ' WHERE query_id = ' . $query . ';');
		if (mysqli_num_rows($result) > 0) {
			$html = '<div style="width: 90%;">';
			$html .= '<table style="width: 99%; table-layout:fixed;" border="1">';
			$html .= '<tr>';
			$html .= '<td align="left" style="width: 6%; word-wrap:break-word;"><b>' . 'Rank' . '</b></td>';
			$html .= '<td align="left" style="width: 33%; word-wrap:break-word;"><b>' . 'Similar phrase as the query' . '</b></td>';
			$html .= '<td align="right" style="width: 22%; word-wrap:break-word;"><b>' . 'Similarity with the query' . '</b></td>';
			$html .= '<td align="right" style="width: 14%; word-wrap:break-word;"><b>' . 'Count of claims' . '</b></td>';
			$html .= '<td align="right" style="width: 25%; word-wrap:break-word;"><b>' . 'Score = similarity * %claim' . '</b></td>';
			$html .= '</tr></table></div>';
			$html .= '<div style="overflow: auto; max-height: 200px; width: 90%;">';
			$html .= '<table style="width: 99%;" border="1">';
			while ($row = mysqli_fetch_object($result)) {
				$html .= '<tr>';
				$html .= '<td align="left" style="width: 6%; word-wrap:break-word;">' . ($row->rank == 0 ? '' : '#' . $row->rank) . '</td>';
				$html .= '<td align="left" style="width: 33%; word-wrap:break-word;"><a href="main.php?dataset=' . $dataset . '&query=' . $row->phrase_id . '&level=' . $level . '#table1">' . $row->phrase . '</a></td>';
				$html .= '<td align="right" style="width: 22%; word-wrap:break-word;">' . number_format($row->similarity, 5, '.', ',') . '</td>';
				$html .= '<td align="right" style="width: 14%; word-wrap:break-word;">' . number_format($row->count_claim, 0, '.', ',') . '</td>';
				$html .= '<td align="right" style="width: 25%; word-wrap:break-word; color:red;">' . number_format($row->score, 5, '.', ',') . '</td>';
				$html .= '</tr>';
			}
			$html .= '</table></div>';
			echo $html;
		} else {
			echo 'We cannot find the <i>query concept</i> (i.e., the group of phrases <i>similar as</i> the query).';
		}
		mysqli_close($conn);
	} else {
		echo 'Connection failed.';
	}
?>
<?php
	echo '<p><a name="table3">Table 3</a>: ASPECTS of the concept of the query <b>' . $query_phrase . '</b>. Please select an aspect:</p>';
	$tablename = $dataset . '_' . $level . '_aspect';
	if ($conn = @mysqli_connect($host, $username, $password)) {
		mysqli_select_db($conn, $dbname);
		$result = mysqli_query($conn, 'SELECT rank, aspect_id, phrase, count_claim, similarity FROM ' . $tablename . ' WHERE query_id = ' . $query . ';');
		if (mysqli_num_rows($result) > 0) {
			$html = '<div style="width: 90%;">';
			$html .= '<table style="width: 99%; table-layout:fixed;" border="1">';
			$html .= '<tr>';
			$html .= '<td align="left" style="width: 6%; word-wrap:break-word;"><b>' . 'Rank' . '</b></td>';
			$html .= '<td align="left" style="width: 58%; word-wrap:break-word;"><b>' . 'The most representative phrase of the aspect' . '</b></td>';
			$html .= '<td align="right" style="width: 22%; word-wrap:break-word;"><b>' . 'Similarity with the query' . '</b></td>';
			$html .= '<td align="right" style="width: 14%; word-wrap:break-word;"><b>' . 'Count of claims' . '</b></td>';
			$html .= '</tr></table></div>';
			$html .= '<div style="overflow: auto; max-height: 200px; width: 90%;">';
			$html .= '<table style="width: 99%; table-layout:fixed;" border="1">';
			while ($row = mysqli_fetch_object($result)) {
				$html .= '<tr ' . ($aspect == $row->aspect_id ? 'style="background-color:yellow" id="selected_aspect"' : '') . '>';
				$html .= '<td align="left" style="width: 6%; word-wrap:break-word;"><a href="main.php?dataset=' . $dataset . '&query=' . $query . '&level=' . $level . '&aspect=' . $row->aspect_id . '#table3">' . '#' . $row->rank . '</a></td>';
				$html .= '<td align="left" style="width: 58%; word-wrap:break-word;">' . $row->phrase . '</td>';
				$html .= '<td align="right" style="width: 22%; word-wrap:break-word;">' . number_format($row->similarity, 5, '.', ',') . '</td>';
				$html .= '<td align="right" style="width: 14%; word-wrap:break-word; color:red;">' . number_format($row->count_claim, 0, '.', ',') . '</td>';
				$html .= '</tr>';
			}
			$html .= '</table></div>';
			$html .= '<script>';
			$html .= 'var selected_aspect=document.getElementById("selected_aspect");';
			$html .= 'selected_aspect.scrollIntoView();';
			$html .= '</script>';
			echo $html;
		} else {
			echo 'We cannot find the <i>aspects</i> (i.e., the phrase groups <i>related to</i> the query).';
		}
		mysqli_close($conn);
	} else {
		echo 'Connection failed.';
	}
?>
<?php
	if ($aspect < 0) {
		for ($i = 0; $i < 30; $i++) {
			echo '<br />';
		}
		return;
	}
	echo '<p><a name="table4">Table 4</a>: PHRASES for the SELECTED ASPECT of the query <b>' . $query_phrase . '</b>.';
	$tablename = $dataset . '_' . $level . '_aspect';
	if ($conn = @mysqli_connect($host, $username, $password)) {
		mysqli_select_db($conn, $dbname);
		$result = mysqli_query($conn, 'SELECT rank, count_claim FROM ' . $tablename . ' WHERE query_id = ' . $query . ' AND aspect_id = ' . $aspect . ';');
		if (mysqli_num_rows($result) > 0) {
			while ($row = mysqli_fetch_object($result)) {
				echo ' We find <b style="color:red">' . number_format($row->count_claim, 0, '.', ',') . '</b> claims on the aspect <b style="color:red">#' . $row->rank . '</b>.';
				break;
			}
		} else {
			echo 'We cannot find the <i>select aspect</i>.';
		}
		mysqli_close($conn);
	} else {
		echo 'Connection failed.';
	}
	echo '</p>';
	$tablename = $dataset . '_' . $level . '_term';
	if ($conn = @mysqli_connect($host, $username, $password)) {
		mysqli_select_db($conn, $dbname);
		$result = mysqli_query($conn, 'SELECT rank, phrase_id, phrase, score, count_claim, similarity FROM ' . $tablename . ' WHERE query_id = ' . $query . ' AND aspect_id = ' . $aspect . ';');
		if (mysqli_num_rows($result) > 0) {
			$html = '<div style="width: 90%;">';
			$html .= '<table style="width: 99%; table-layout:fixed;" border="1">';
			$html .= '<tr>';
			$html .= '<td align="left" style="width: 6%; word-wrap:break-word;"><b>' . 'Rank' . '</b></td>';
			$html .= '<td align="left" style="width: 44%; word-wrap:break-word;"><b>' . 'Phrase for the selected aspect' . '</b></td>';
			$html .= '<td align="right" style="width: 22%; word-wrap:break-word;"><b>' . 'Similarity with the query' . '</b></td>';
			$html .= '<td align="right" style="width: 14%; word-wrap:break-word;"><b>' . 'Count of claims' . '</b></td>';
			$html .= '<td align="right" style="width: 14%; word-wrap:break-word;"><b>' . 'Score = %claim' . '</b></td>';
			$html .= '</tr></table></div>';
			$html .= '<div style="overflow: auto; max-height: 200px; width: 90%;">';
			$html .= '<table style="width: 99%; table-layout:fixed;" border="1">';
			while ($row = mysqli_fetch_object($result)) {
				$html .= '<tr>';
				$html .= '<td align="left" style="width: 6%; word-wrap:break-word;">' . '#' . $row->rank. '</td>';
				$html .= '<td align="left" style="width: 44%; word-wrap:break-word;"><a href="main.php?dataset=' . $dataset . '&query=' . $row->phrase_id . '&level=' . $level . '#table1">' . $row->phrase . '</a></td>';
				$html .= '<td align="right" style="width: 22%; word-wrap:break-word;">' . number_format($row->similarity, 5, '.', ',') . '</td>';
				$html .= '<td align="right" style="width: 14%; word-wrap:break-word;">' . number_format($row->count_claim, 0, '.', ',') . '</td>';
				$html .= '<td align="right" style="width: 14%; word-wrap:break-word; color:red;">' . number_format($row->score, 5, '.', ',') . '</td>';
				$html .= '</tr>';
			}
			$html .= '</table></div>';
			echo $html;
		} else {
			echo 'We cannot find the <i>aspect concept</i> (i.e., the group of similar phrases to represent the aspect).';
		}
		mysqli_close($conn);
	} else {
		echo 'Connection failed.';
	}
?>
<?php
	echo '<p><a name="table5">Table 5</a>: CLAIMS for the SELECTED ASPECT of the query <b>' . $query_phrase . '</b>. Please select a claim for a complete document:</p>';
	$tablename = $dataset . '_' . $level . '_claim';
	if ($conn = @mysqli_connect($host, $username, $password)) {
		mysqli_select_db($conn, $dbname);
		$result = mysqli_query($conn, 'SELECT rank, claim_id, claim, score FROM ' . $tablename . ' WHERE query_id = ' . $query . ' AND aspect_id = ' . $aspect . ';');
		if (mysqli_num_rows($result) > 0) {
			$html = '<div style="width: 90%;">';
			$html .= '<table style="width: 99%; table-layout:fixed;" border="1">';
			$html .= '<tr>';
			$html .= '<td align="left" style="width: 6%; word-wrap:break-word;"><b>' . 'Rank' . '</b></td>';
			$html .= '<td align="left" style="width: 85%; word-wrap:break-word;"><b>' . 'Claim' . '</b></td>';
			$html .= '<td align="right" style="width: 9%; word-wrap:break-word;"><b>' . 'Score' . '</b></td>';
			$html .= '</tr></table></div>';
			$html .= '<div style="overflow: auto; max-height: 200px; width: 90%;">';
			$html .= '<table style="width: 99%; table-layout:fixed;" border="1">';
			while ($row = mysqli_fetch_object($result)) {
				$html .= '<tr ' . ($claim == $row->claim_id ? 'style="background-color:yellow" id="selected_claim"' : '') . '>';
				$html .= '<td align="left" style="width: 6%; word-wrap:break-word;"><a href="main.php?dataset=' . $dataset . '&query=' . $query . '&level=' . $level . '&aspect=' . $aspect . '&claim=' . $row->claim_id . '#table5">' . '#' . $row->rank . '</a></td>';
				$html .= '<td align="left" style="width: 85%; word-wrap:break-word;">' . $row->claim . '</td>';
				$html .= '<td align="right" style="width: 9%; word-wrap:break-word; color:red;">' . number_format($row->score, 5, '.', ',') . '</td>';
				$html .= '</tr>';
				if ($claim == $row->claim_id) $sentence = $row->claim;
			}
			$html .= '</table></div>';
			$html .= '<script>';
			$html .= 'var selected_claim=document.getElementById("selected_claim");';
			$html .= 'selected_claim.scrollIntoView();';
			$html .= '</script>';
			echo $html;
		} else {
			echo 'We cannot find the <i>aspect claims</i> (i.e., the list of claims to represent the aspect).';
		}
		mysqli_close($conn);
	} else {
		echo 'Connection failed.';
	}
?>
<?php
	if ($claim < 0) {
		for ($i = 0; $i < 30; $i++) {
			echo '<br />';
		}
		return;
	}
	echo '<p><a name="table6">Table 6</a>: the SELECTED CLAIM and the complete DOCUMENT. </p>';
	if ($conn = @mysqli_connect($host, $username, $password)) {
		mysqli_select_db($conn, $dbname);
		$tablename = $dataset . '_claim2document';
		$result = mysqli_query($conn, 'SELECT document_id FROM ' . $tablename . ' WHERE claim_id = ' . $claim . ';');
		if (mysqli_num_rows($result) > 0) {
			while ($row = mysqli_fetch_object($result)) {
				$document_id = $row->document_id;
				break;
			}
		} else {
			echo 'We cannot find the <i>document</i>.';
		}

		$tablename = $dataset . '_document';
		$result = mysqli_query($conn, 'SELECT document FROM ' . $tablename . ' WHERE document_id = ' . $document_id . ';');
		if (mysqli_num_rows($result) > 0) {
			while ($row = mysqli_fetch_object($result)) {
				$document = $row->document;
				break;
			}
		} else {
			echo 'We cannot find the <i>document</i>.';
		}
		mysqli_close($conn);
	} else {
		echo 'Connection failed.';
	}
	$html = '<div style="overflow: auto; width: 90%;">';
	$html .= '<table style="width: 99%;" border="1">';
	$html .= '<tr>';
	$html .= '<td align="left"><b>' . 'Selected claim' . '</b></td>';
	$html .= '<td align="left">' . $sentence . '</td>';
	$html .= '</tr>';
	$html .= '<tr>';
	$html .= '<td align="left"><b>' . 'Document' . '</b></td>';
	$html .= '<td align="left">' . (isset($document) ? $document : 'NULL') . '</td>';
	$html .= '</tr>';
	$html .= '</table></div>';
	echo $html;
?>
<?php
	for ($i = 0; $i < 30; $i++) {
		echo '<br />';
	}
?>
	</body>
</html>

