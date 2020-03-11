var paginator = document.querySelectorAll('.paginator');
var SHOWN_NUMBER = 20;
var first = true;
var SHOWN_PAGES = 10;

var makeEl = function(tag , classX , txt = '') {
	var item = document.createElement(tag);
	item.classList.add(classX);
	if (txt !== '' && txt!== '<<' && txt!== '>>') {
		item.textContent = txt+1;
	}
	if (txt === '<<' || txt === '>>') {
		item.textContent = txt;
	}
	return item;
}

var selectPage = function(idl , pag , btnListChild) {
	idl--;
	for (var i = 0; i < pag.length; i++) {
		if (!pag[i].classList.contains('hidden')) {
			console.log(pag[i]);
			pag[i].classList.add('hidden');
		}
	}
	for (var i = SHOWN_NUMBER*idl; i < Math.min(pag.length , SHOWN_NUMBER*idl + SHOWN_NUMBER); i++) {
		pag[i].classList.remove('hidden');
		console.log(pag[i]);
	}
	for (var i = 0; i < btnListChild.length; i++) {
		if (!btnListChild[i].classList.contains('hidden')) {
			console.log(btnListChild[i]);
			btnListChild[i].classList.add('hidden');
		}
	}
	for (var i = Math.max(idl - SHOWN_PAGES/2 , 0); i < Math.min(idl + SHOWN_PAGES/2 , btnListChild.length) ; i++) {
		console.log(btnListChild[i]);
		btnListChild[i].classList.remove('hidden');
	}
	console.log(btnListChild)
}

var paginatorUse = function() {
    for (var i = 0; i < paginator.length; i++) {
	first = true;
	var pag = paginator[i].querySelectorAll('.problem');
	console.log(pag);
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
		console.log(curParent);
		var lastBtn = curParent.querySelector('.currentButton');
		lastBtn.classList.remove('currentButton');
		curParent.firstChild.classList.add('currentButton');
		selectPage(1 , this.pag , this.btnListChild);
	});
	var lastPage = makeEl('button' , 'pgn-btn' , '>>');
	lastPage.pag = pag;
	lastPage.btnListChild = btnListChild;
	lastPage.addEventListener('click' , function(evt) {
		evt.preventDefault();

		var curParent = evt.currentTarget.previousSibling;
		console.log(curParent);
		var lastBtn = curParent.querySelector('.currentButton');
		lastBtn.classList.remove('currentButton');
		curParent.lastChild.classList.add('currentButton');
		selectPage(this.btnListChild.length , this.pag , this.btnListChild);
	});
	paginator[i].appendChild(allBtnList);
	allBtnList.appendChild(stPage);
	allBtnList.appendChild(btnList);
	allBtnList.appendChild(lastPage);
	for (var j = 0; j < pag.length / SHOWN_NUMBER; j++) {
		var curPage = makeEl('div' , 'page');
		var curBtn = makeEl('button' , 'pgn-btn' , j);
		curBtn.pag = pag;
		curBtn.btnListChild = btnListChild;
		paginator[i].appendChild(curPage);
		btnList.appendChild(curBtn);
		curBtn.addEventListener('click' , function(evt) {
			evt.preventDefault();

			var curParent = evt.currentTarget.parentElement;
			var lastBtn = curParent.querySelector('.currentButton');
			console.log(lastBtn);
			lastBtn.classList.remove('currentButton');
			evt.currentTarget.classList.add('currentButton');
			selectPage(evt.currentTarget.textContent , this.pag , this.btnListChild);
		});
	}
	if (first === true) {
		selectPage(1 , pag , btnListChild);
		btnList.firstChild.classList.add('currentButton');
		first = false;
	}
}
}

window.onload = function() {
	console.log(paginator);
    paginatorUse();
}