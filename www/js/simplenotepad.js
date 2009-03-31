SN = {};


$(document).ready(function() {
	SN.initDelete();
	SN.toggleCheatsheet();
});

SN.toggleCheatsheet = function() {
	$('#cheatsheetToggle').click(function() {
		$('#cheatsheet').toggle();
		return false;
	});
};

SN.initDelete = function() {
	$('#todos').find("a[class='delete']").click(function() {
		if (confirm('are you sure?')) {
			var del_o = {
				'url': $(this).attr('href'),
				'type':'DELETE',
			'complete': function() { location.reload(); },
			};
			$.ajax(del_o);
		}
		return false;
	});
};
