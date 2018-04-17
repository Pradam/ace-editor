$(document).ready(function(){

			$('ul.mtree').mtree({
				collapsed: true, // Start with collapsed menu (only level 1 items visible)
				close_same_level: false, // Close elements on same level when opening new node.
			});

			
			$('li').draggable({ opacity: 0.7, helper: "clone" });
			
	
			$('#code-editor').droppable({
		      drop: function( event, ui ) {
				ui.draggable[0]['innerText']
				var $data = $('#code-editor').val();
				$data = $data + ' ' + ui.draggable[0]['innerText'];
				$('#code-editor').val($data);
			  }
			});


});
