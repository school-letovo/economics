var paginators = document.querySelectorAll(".paginator");
var amounts = document.querySelectorAll('.paginator-amount');
var SHOWN_PAGES = 10;
var SHOWN_NUMBER = 20;

var sendRequest = function(method , url) {
    return new Promise((resolve, reject) => {
        var xhr = new XMLHttpRequest();

        xhr.open(method , url);

        xhr.responseType= 'text';

        xhr.onload = () => {
            if (xhr.status>=400) {
                reject(xhr.response);
            }
            else {
                resolve(xhr.response);
            }
        };

        xhr.onerror = () => {
            reject(xhr.response);
        };

        xhr.send()
    });
};

var createUrl = function(type,page,number) {
  return '/problems/'+type+'/'+page+'/'+number
};

var makeEl = function (tag, classX, txt = '') {
	var item = document.createElement(tag);
	item.classList.add(classX);
	item.textContent = txt;
	return item;
};

var recreatePaginator = function (curBtn,pag,numList,SHOWN_NUMBER) {
    sendRequest('GET', createUrl(pag.id,curBtn,SHOWN_NUMBER))
        .then(data => {
            data = JSON.parse(data);
            pag.innerHTML = data['html'];
            var curLen = data['length'];
            var len = 0;
	        if (curLen % SHOWN_NUMBER !== 0) {
                len = Math.floor(curLen / SHOWN_NUMBER) + 1;
            } else {
                len = curLen / SHOWN_NUMBER;
            }
            numList.innerHTML = "";
            for (var i = Math.max(curBtn - SHOWN_PAGES/2 , 1); i <= Math.min(parseInt(curBtn) + SHOWN_PAGES/2 , len) ; i++) {
                var newBtn = makeEl('button', 'pgn-btn', i);
                if (curBtn - i === 0) {
                    newBtn.classList.add('currentButton');
                }
                newBtn.addEventListener('click', function (evt) {
                    evt.preventDefault();

                    recreatePaginator(this.textContent, pag, numList,SHOWN_NUMBER);
                });
                numList.appendChild(newBtn);
            }
        });
};

var filterRecreate = function (paginator,resistor,SHOWN_NUMBER) {
    sendRequest('GET', createUrl(paginator.id,1,SHOWN_NUMBER))
        .then(data => {
            data = JSON.parse(data);
            paginator.innerHTML = data['html'];
            resistor.innerHTML = "";
            var curLen = data['length'];
            var len = 0;
	        if (curLen % SHOWN_NUMBER !== 0) {
                len = Math.floor(curLen / SHOWN_NUMBER) + 1;
            } else {
                len = curLen / SHOWN_NUMBER;
            }
            var btnList = makeEl('div', 'inline');
            var numList = makeEl('div','inline');
            var filters = makeEl('div', 'inline');
            var chooseFilter = makeEl('p' , 'chooseFilter' , 'Показывать по:');
            var stPage = makeEl('button', 'pgn-btn','<<');
            stPage.addEventListener('click', function (evt) {
                evt.preventDefault();

                recreatePaginator(1, paginator, numList,SHOWN_NUMBER);
            });
            var ltPage = makeEl('button', 'phn-btn','>>');
            ltPage.addEventListener('click', function (evt) {
                evt.preventDefault();

                recreatePaginator(len, paginator, numList,SHOWN_NUMBER);
            });
            var filterFive = makeEl('button', 'filter-btn', '5');
            filterFive.addEventListener('click', function (evt) {
                evt.preventDefault();

                filterRecreate(paginator, resistor,5);
            });
            var filterTwenty = makeEl('button', 'filter-btn', '20');
            filterTwenty.addEventListener('click', function (evt) {
                evt.preventDefault();

                filterRecreate(paginator, resistor,20);
            });
            var filterHundred = makeEl('button', 'filter-btn', '100');
            filterHundred.addEventListener('click', function (evt) {
                evt.preventDefault();

                filterRecreate(paginator, resistor,100);
            });
            if (SHOWN_NUMBER === 5) {
		        filterFive.classList.add('currentButton');
	        }
            if (SHOWN_NUMBER === 20) {
		        filterTwenty.classList.add('currentButton');
	        }
	        if (SHOWN_NUMBER === 100) {
		        filterHundred.classList.add('currentButton');
	        }
            var first = true;
            for (var j = 1; j<=Math.min(len, 1+SHOWN_PAGES/2); j++) {
                var newBtn = makeEl('button', 'pgn-btn', j);
                if (first) {
                    newBtn.classList.add('currentButton');
                    first = false;
                }
                newBtn.addEventListener('click', function (evt) {
                    evt.preventDefault();

                    recreatePaginator(this.textContent, paginator, numList,SHOWN_NUMBER);
                });
                numList.appendChild(newBtn);
            }
            filters.appendChild(filterFive);
            filters.appendChild(filterTwenty);
            filters.appendChild(filterHundred);
            btnList.appendChild(stPage);
            btnList.appendChild(numList);
            btnList.appendChild(ltPage);
            resistor.appendChild(btnList);
            resistor.appendChild(chooseFilter);
            resistor.appendChild(filters);
        });
};

var createPaginator = async function (paginator,SHOWN_NUMBER,amount) {
    await sendRequest('GET', createUrl(paginator.id,1,SHOWN_NUMBER))
        .then(data => {
            data = JSON.parse(data);
            paginator.innerHTML = data['html'];
            var curLen = data['length'];
            amount.textContent = amount.textContent+curLen+')';
            var len = 0;
	        if (curLen % SHOWN_NUMBER !== 0) {
                len = Math.floor(curLen / SHOWN_NUMBER) + 1;
            } else {
                len = curLen / SHOWN_NUMBER;
            }
            var resistor = makeEl('div', 'resistor');
            var btnList = makeEl('div', 'inline');
            var numList = makeEl('div','inline');
            var filters = makeEl('div', 'inline');
            var chooseFilter = makeEl('p' , 'chooseFilter' , 'Показывать по:');
            var stPage = makeEl('button', 'pgn-btn','<<');
            stPage.addEventListener('click', function (evt) {
                evt.preventDefault();

                recreatePaginator(1, paginator, numList,SHOWN_NUMBER);
            });
            var ltPage = makeEl('button', 'phn-btn','>>');
            ltPage.addEventListener('click', function (evt) {
                evt.preventDefault();

                recreatePaginator(len, paginator, numList,SHOWN_NUMBER);
            });
            var filterFive = makeEl('button', 'filter-btn', '5');
            filterFive.addEventListener('click', function (evt) {
                evt.preventDefault();

                filterRecreate(paginator, resistor,5);
            });
            var filterTwenty = makeEl('button', 'filter-btn', '20');
            filterTwenty.addEventListener('click', function (evt) {
                evt.preventDefault();

                filterRecreate(paginator, resistor,20);
            });
            var filterHundred = makeEl('button', 'filter-btn', '100');
            filterHundred.addEventListener('click', function (evt) {
                evt.preventDefault();

                filterRecreate(paginator, resistor,100);
            });
            if (SHOWN_NUMBER === 5) {
		        filterFive.classList.add('currentButton');
	        }
            if (SHOWN_NUMBER === 20) {
		        filterTwenty.classList.add('currentButton');
	        }
	        if (SHOWN_NUMBER === 100) {
		        filterHundred.classList.add('currentButton');
	        }
            var first = true;
            for (var j = 1; j<=Math.min(len, 1+SHOWN_PAGES/2); j++) {
                var newBtn = makeEl('button', 'pgn-btn', j);
                if (first) {
                    newBtn.classList.add('currentButton');
                    first = false;
                }
                newBtn.addEventListener('click', function (evt) {
                    evt.preventDefault();

                    recreatePaginator(this.textContent, paginator, numList,SHOWN_NUMBER);
                });
                numList.appendChild(newBtn);
            }
            filters.appendChild(filterFive);
            filters.appendChild(filterTwenty);
            filters.appendChild(filterHundred);
            btnList.appendChild(stPage);
            btnList.appendChild(numList);
            btnList.appendChild(ltPage);
            resistor.appendChild(btnList);
            resistor.appendChild(chooseFilter);
            resistor.appendChild(filters);
            paginator.parentElement.appendChild(resistor);
        });
};

var startFunction = async function(paginators,amounts) {
    for (var i = 0; i < paginators.length; i++) {
        await createPaginator(paginators[i],SHOWN_NUMBER,amounts[i]);
    }
};

window.onload = function () {
    startFunction(paginators,amounts);
};