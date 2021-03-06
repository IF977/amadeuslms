$('#id_groups').multiSelect({
  selectableHeader: "<input type='text' class='search-input category-search-users' autocomplete='off' placeholder=' '>",
  selectionHeader: "<input type='text' class='search-input category-search-users' autocomplete='off' placeholder=''>",
  afterInit: function(ms){
	var that = this,
		$selectableSearch = that.$selectableUl.prev(),
		$selectionSearch = that.$selectionUl.prev(),
		selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
		selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';

	that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
	.on('keydown', function(e){
	  if (e.which === 40){
		that.$selectableUl.focus();
		return false;
	  }
	});

	that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
	.on('keydown', function(e){
	  if (e.which == 40){
		that.$selectionUl.focus();
		return false;
	  }
	});
  },
  afterSelect: function(){
	this.qs1.cache();
	this.qs2.cache();
  },
  afterDeselect: function(){
	this.qs1.cache();
	this.qs2.cache();
  }
});// Used to create multi-select css style

$('#id_students').multiSelect({
  selectableHeader: "<input type='text' class='search-input category-search-users' autocomplete='off' placeholder=' '>",
  selectionHeader: "<input type='text' class='search-input category-search-users' autocomplete='off' placeholder=''>",
  afterInit: function(ms){
	var that = this,
		$selectableSearch = that.$selectableUl.prev(),
		$selectionSearch = that.$selectionUl.prev(),
		selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
		selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';

	that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
	.on('keydown', function(e){
	  if (e.which === 40){
		that.$selectableUl.focus();
		return false;
	  }
	});

	that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
	.on('keydown', function(e){
	  if (e.which == 40){
		that.$selectionUl.focus();
		return false;
	  }
	});
  },
  afterSelect: function(){
	this.qs1.cache();
	this.qs2.cache();
  },
  afterDeselect: function(){
	this.qs1.cache();
	this.qs2.cache();
  }
});// Used to create multi-select css style

$('.collapse').on('show.bs.collapse', function (e) {
	if($(this).is(e.target)){
		var btn = $(this).parent().find('.fa-angle-right');

		btn.switchClass("fa-angle-right", "fa-angle-down", 250, "easeInOutQuad");
	}
});

$('.collapse').on('hide.bs.collapse', function (e) {
	if($(this).is(e.target)){
		var btn = $(this).parent().find('.fa-angle-down');

		btn.switchClass("fa-angle-down", "fa-angle-right", 250, "easeInOutQuad");
	}
});

$('.begin_date_input').on('click', function () {
	var checkbox = $(this).parent().parent().find('.begin_date');

	$(checkbox).prop('checked', true);
});

$('.end_date_input').on('click', function () {
	var checkbox = $(this).parent().parent().find('.end_date');

	$(checkbox).prop('checked', true);
});

$('.limit_date_input').on('click', function () {
	var checkbox = $(this).parent().parent().find('.limit_date');

	$(checkbox).prop('checked', true);
});

// check if browser supports drag n drop
// call initialization file
if (window.File && window.FileList && window.FileReader) {
	Init();
}

// initialize
function Init() {
	var small = $(".file-selector"),
		filedrag = $(".filedrag"),
		common = $(".common-file-input");
		
	// file select
	small.on("change", FileSelectHandler);

	// is XHR2 available?
	var xhr = new XMLHttpRequest();
	if (xhr.upload) {
		// file drop
		filedrag.on("drop", FileSelectHandler);
		filedrag.attr('style', 'display:block');
		common.attr('style', 'display:none');
	}
}

// file selection
function FileSelectHandler(e) {
	var files = e.target.files || e.dataTransfer.files,
		parent = $(e.target.offsetParent);

	// process all File objects
	for (var i = 0, f; f = files[i]; i++) {
		parent.find('.filedrag').html(f.name);
	}
}