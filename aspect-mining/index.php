<html>
	<head>
		<title>Select a dataset</title>
	</head>
	<body>
<?php include('connect.php'); ?>
	<p><b>Concept-level aspect mining</b></p>
	<p>Please select a dataset:</p>
<?php
	if ($conn = @mysqli_connect($host, $username, $password)) {
		mysqli_select_db($conn, $dbname);
		$result = mysqli_query($conn, 'SELECT dataset,num_document,num_sentence,num_phrase,count_char,count_phrase,count_char_per_document,count_char_per_sentence,count_phrase_per_document,count_phrase_per_sentence FROM dataset;');
		if (mysqli_num_rows($result) > 0) {
			$html = '<table style="width: 90%;" border="1">';
			$html .= '<tr>';
			$html .= '<td align="left"><b>' . 'Data set' . '</b></td>';
			$html .= '<td align="right"><b>' . 'Number of documents' . '</b></td>';
			$html .= '<td align="right"><b>' . 'Number of sentences' . '</b></td>';
			$html .= '<td align="right"><b>' . 'Number of phrases' . '</b></td>';
			$html .= '<td align="right"><b>' . 'Count of bytes (chars)' . '</b></td>';
			$html .= '<td align="right"><b>' . 'Count of phrases' . '</b></td>';
			$html .= '<td align="right"><b>' . 'Count of bytes per document' . '</b></td>';
			$html .= '<td align="right"><b>' . 'Count of bytes per sentence' . '</b></td>';
			$html .= '<td align="right"><b>' . 'Count of phrases per document' . '</b></td>';
			$html .= '<td align="right"><b>' . 'Count of phrases per sentence' . '</b></td>';
			$html .= '</tr>';
			while ($row = mysqli_fetch_object($result)) {
				$html .= '<tr>';
				$html .= '<td align="left"><a href="main.php?dataset=' . $row->dataset . '">' . $row->dataset . '</a></td>';
				$html .= '<td align="right">' . number_format($row->num_document, 0, '.', ',') . '</td>';
				$html .= '<td align="right">' . number_format($row->num_sentence, 0, '.', ',') . '</td>';
				$html .= '<td align="right">' . number_format($row->num_phrase, 0, '.', ',') . '</td>';
				$html .= '<td align="right">' . number_format($row->count_char, 0, '.', ',') . '</td>';
				$html .= '<td align="right">' . number_format($row->count_phrase, 0, '.', ',') . '</td>';
				$html .= '<td align="right">' . number_format($row->count_char_per_document, 2, '.', ',') . '</td>';
				$html .= '<td align="right">' . number_format($row->count_char_per_sentence, 2, '.', ',') . '</td>';
				$html .= '<td align="right">' . number_format($row->count_phrase_per_document, 2, '.', ',') . '</td>';
				$html .= '<td align="right">' . number_format($row->count_phrase_per_sentence, 2, '.', ',') . '</td>';
				$html .= '</tr>';
			}
			$html .= '</table>';
			echo $html;
		} else {
			echo 'We cannot find any dataset.';
		}
		mysqli_close($conn);
	} else {
		echo 'Connection failed.';
	}
?>
	</body>
</html>

