var paginator = document.querySelectorAll('.paginator');
var SHOWN_NUMBER = 20;
var first = true;
var SHOWN_PAGES = 10;

var makeEl = function(tag , classX , txt = '' , filterFlag = false) {
	var item = document.createElement(tag);
	item.classList.add(classX);
	if (txt !== '' && txt!== '<<' && txt!== '>>' && filterFlag === false) {
		item.textContent = txt+1;
	}
	if (txt === '<<' || txt === '>>' || filterFlag === true) {
		item.textContent = txt;
	}
	return item;
};

var selectPage = function(idl , pag , btnListChild, SHOWN_NUMBER) {
	idl--;
	for (var i = 0; i < pag.length; i++) {
		if (!pag[i].classList.contains('hidden')) {
			pag[i].classList.add('hidden');
		}
	}
	for (var i = SHOWN_NUMBER*idl; i < Math.min(pag.length , SHOWN_NUMBER*idl + SHOWN_NUMBER); i++) {
		pag[i].classList.remove('hidden');
	}
	for (var i = 0; i < btnListChild.length; i++) {
		if (!btnListChild[i].classList.contains('hidden')) {
			btnListChild[i].classList.add('hidden');
		}
	}
	for (var i = Math.max(idl - SHOWN_PAGES/2 , 0); i < Math.min(idl + SHOWN_PAGES/2 , btnListChild.length) ; i++) {
		btnListChild[i].classList.remove('hidden');
	}
};

var paginatorUse = function(SHOWN_NUMBER) {
	for (var i = 0; i < paginator.length; i++) {
		first = true;
		var pag = paginator[i].querySelectorAll('.problem');
		var resistor = makeEl('div', 'resistor');
		var chooseFilter = makeEl('p', 'chooseFilter', 'Показывать по:', true);
		var filter = makeEl('div', 'inline');
		var allBtnList = makeEl('div', 'inline');
		var btnList = makeEl('div', 'inline');
		btnList.classList.add('btnList');
		var btnListChild = btnList.childNodes;
		var stPage = makeEl('button', 'pgn-btn', '<<');
		stPage.pag = pag;
		stPage.btnListChild = btnListChild;
		stPage.addEventListener('click', function (evt) {
			evt.preventDefault();

			var curParent = evt.currentTarget.nextSibling;
			var lastBtn = curParent.querySelector('.currentButton');
			lastBtn.classList.remove('currentButton');
			curParent.firstChild.classList.add('currentButton');
			selectPage(1, this.pag, this.btnListChild, SHOWN_NUMBER);
		});
		var lastPage = makeEl('button', 'pgn-btn', '>>');
		lastPage.pag = pag;
		lastPage.btnListChild = btnListChild;
		lastPage.SHOWN_NUMBER = SHOWN_NUMBER;
		lastPage.addEventListener('click', function (evt) {
			evt.preventDefault();

			var curParent = evt.currentTarget.previousSibling;
			var lastBtn = curParent.querySelector('.currentButton');
			lastBtn.classList.remove('currentButton');
			curParent.lastChild.classList.add('currentButton');
			selectPage(this.btnListChild.length, this.pag, this.btnListChild, SHOWN_NUMBER);
		});
		var filterFive = makeEl('button', 'pgn-btn', '5', true);
		filterFive.idk = i;
		filterFive.addEventListener('click', function (evt) {
			evt.preventDefault();

			evt.currentTarget.parentElement.parentElement.remove();
			paginatorUseOne(this.idk, 5);
		});
		var filterTwenty = makeEl('button', 'pgn-btn', '20', true);
		filterTwenty.idk = i;
		filterTwenty.addEventListener('click', function (evt) {
			evt.preventDefault();

			evt.currentTarget.parentElement.parentElement.remove();
			paginatorUseOne(this.idk, 20);
		});
		var filterHundred = makeEl('button', 'pgn-btn', '100', true);
		filterHundred.idk = i;
		filterHundred.addEventListener('click', function (evt) {
			evt.preventDefault();

			evt.currentTarget.parentElement.parentElement.remove();
			paginatorUseOne(this.idk, 100);
		});
		paginator[i].appendChild(resistor);
		resistor.appendChild(allBtnList);
		resistor.appendChild(chooseFilter);
		resistor.appendChild(filter);
		allBtnList.appendChild(stPage);
		allBtnList.appendChild(btnList);
		allBtnList.appendChild(lastPage);
		filter.appendChild(filterFive);
		filter.appendChild(filterTwenty);
		filter.appendChild(filterHundred);
		for (var j = 0; j < pag.length / SHOWN_NUMBER; j++) {
			var curPage = makeEl('div', 'page');
			var curBtn = makeEl('button', 'pgn-btn', j);
			curBtn.pag = pag;
			curBtn.btnListChild = btnListChild;
			paginator[i].appendChild(curPage);
			btnList.appendChild(curBtn);
			curBtn.addEventListener('click', function (evt) {
				evt.preventDefault();

				var curParent = evt.currentTarget.parentElement;
				var lastBtn = curParent.querySelector('.currentButton');
				lastBtn.classList.remove('currentButton');
				evt.currentTarget.classList.add('currentButton');
				selectPage(evt.currentTarget.textContent, this.pag, this.btnListChild, SHOWN_NUMBER);
			});
		}
		if (first === true) {
			selectPage(1, pag, btnListChild, SHOWN_NUMBER);
			btnList.firstChild.classList.add('currentButton');
			first = false;
		}
		filterTwenty.classList.add('currentButton');
	}
	;
}

var paginatorUseOne = function(idk , SHOWN_NUMBER) {
	first = true;
	var pag = paginator[idk].querySelectorAll('.problem');
	var resistor = makeEl('div' , 'resistor');
	var chooseFilter = makeEl('p' , 'chooseFilter' , 'Показывать по:' , true);
	var filter = makeEl('div' , 'inline');
	var allBtnList = makeEl('div' , 'inline');
	var btnList = makeEl('div' , 'inline');
	btnList.classList.add('btnList');
	var btnListChild = btnList.childNodes;
	var stPage = makeEl('button' , 'pgn-btn' , '<<');
	stPage.pag = pag;
	stPage.btnListChild = btnListChild;
	stPage.addEventListener('click' , function(evt) {
		evt.preventDefault();

		var curParent = evt.currentTarget.nextSibling;
		var lastBtn = curParent.querySelector('.currentButton');
		lastBtn.classList.remove('currentButton');
		curParent.firstChild.classList.add('currentButton');
		selectPage(1 , this.pag , this.btnListChild, SHOWN_NUMBER);
	});
	var lastPage = makeEl('button' , 'pgn-btn' , '>>');
	lastPage.pag = pag;
	lastPage.btnListChild = btnListChild;
	lastPage.SHOWN_NUMBER = SHOWN_NUMBER;
	lastPage.addEventListener('click' , function(evt) {
		evt.preventDefault();

		var curParent = evt.currentTarget.previousSibling;
		var lastBtn = curParent.querySelector('.currentButton');
		lastBtn.classList.remove('currentButton');
		curParent.lastChild.classList.add('currentButton');
		selectPage(this.btnListChild.length , this.pag , this.btnListChild , SHOWN_NUMBER);
	});
	var filterFive = makeEl('button' , 'pgn-btn' , '5' , true);
	filterFive.idk = idk;
	filterFive.addEventListener('click' , function(evt) {
		evt.preventDefault();

		evt.currentTarget.parentElement.parentElement.remove();
		paginatorUseOne(this.idk , 5);
	});
	var filterTwenty = makeEl('button' , 'pgn-btn' , '20' , true);
	filterTwenty.idk = idk;
	filterTwenty.addEventListener('click' , function(evt) {
		evt.preventDefault();

		evt.currentTarget.parentElement.parentElement.remove();
		paginatorUseOne(this.idk , 20);
	});
	var filterHundred = makeEl('button' , 'pgn-btn' , '100' , true);
	filterHundred.idk = idk;
	filterHundred.addEventListener('click' , function(evt) {
		evt.preventDefault();

		evt.currentTarget.parentElement.parentElement.remove();
		paginatorUseOne(this.idk , 100);
	});
	paginator[idk].appendChild(resistor);
	resistor.appendChild(allBtnList);
	resistor.appendChild(chooseFilter);
	resistor.appendChild(filter);
	allBtnList.appendChild(stPage);
	allBtnList.appendChild(btnList);
	allBtnList.appendChild(lastPage);
	filter.appendChild(filterFive);
	filter.appendChild(filterTwenty);
	filter.appendChild(filterHundred);
	for (var j = 0; j < pag.length / SHOWN_NUMBER; j++) {
		var curPage = makeEl('div' , 'page');
		var curBtn = makeEl('button' , 'pgn-btn' , j);
		curBtn.pag = pag;
		curBtn.btnListChild = btnListChild;
		paginator[idk].appendChild(curPage);
		btnList.appendChild(curBtn);
		curBtn.addEventListener('click' , function(evt) {
			evt.preventDefault();

			var curParent = evt.currentTarget.parentElement;
			var lastBtn = curParent.querySelector('.currentButton');
			lastBtn.classList.remove('currentButton');
			evt.currentTarget.classList.add('currentButton');
			selectPage(evt.currentTarget.textContent , this.pag , this.btnListChild , SHOWN_NUMBER);
		});
	}
	if (first === true) {
		selectPage(1 , pag , btnListChild , SHOWN_NUMBER);
		btnList.firstChild.classList.add('currentButton');
		first = false;
	}
	if (SHOWN_NUMBER === 5) {
		filterFive.classList.add('currentButton');
	}
	if (SHOWN_NUMBER === 20) {
		filterTwenty.classList.add('currentButton');
	}
	if (SHOWN_NUMBER === 100) {
		filterHundred.classList.add('currentButton');
	}
};

window.onload = function() {
    paginatorUse(SHOWN_NUMBER);
};