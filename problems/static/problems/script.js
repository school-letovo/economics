var paginators = document.querySelectorAll(".paginator");
var amounts = document.querySelectorAll('.paginator-amount');
var createTest = document.querySelector('#createTest');
var assignProb = document.querySelector('#assignProb');
var SHOWN_PAGES = 10;
var SHOWN_NUMBER = 20;
var problem = [];
var student = [];
var counter = 0;


var sendRequest = function(method , url, data) {
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
        xhr.send(data);
    });
};

var createUrl = function(type,page,number) {
  return '/problems/'+type+'/'+page+'/'+number;
};

var makeEl = function (tag, classX, txt = '') {
	var item = document.createElement(tag);
	item.classList.add(classX);
	item.textContent = txt;
	return item;
};

var recreatePaginator = function (curBtn,pag,numList,SHOWN_NUMBER) {
    let fdata = new FormData(document.getElementById('filters'));
    sendRequest('POST', createUrl(pag.id,curBtn,SHOWN_NUMBER), fdata)
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

	        var lastDivs = document.querySelector('.counter');
            lastDivs.innerHTML = "";
            var checkboxes = document.querySelectorAll('.checkbox-check');

            var check = function (checkbox) {
                checkbox.onclick = function() {
		            if (checkbox.checked) {
			            counter++;
                        problem.push(parseInt(checkbox.value));
		            } else {
			            counter--;
                        problem = problem.filter(function(value, index, arr) {
                            return value !== parseInt(checkbox.value);
                        });
		            }
		            span.textContent = counter;
	            };
            };

            var divs = document.querySelector('.counter');
            var clear = document.createElement('button');
            var span = document.createElement('span');
            var selectAll = document.createElement('button');
            selectAll.textContent = "Выбрать всё";
            clear.textContent = "Очистить";

            for (var i = 0; i < checkboxes.length; i++) {
                if (problem.includes(parseInt(checkboxes[i].value)))
                    checkboxes[i].checked = true;
	            check(checkboxes[i]);
            }

            divs.appendChild(span);
            divs.appendChild(clear);
            divs.appendChild(selectAll);
            span.textContent = counter;

            clear.onclick = function(evt) {
	            evt.preventDefault();

	            for (var i = 0; i < checkboxes.length; i++) {
		            checkboxes[i].checked = false;
	            }

                problem = [];
	            counter = 0;
	            span.textContent = counter;
            };

            selectAll.addEventListener('click' , function(evt) {
	            evt.preventDefault();

                let checked = 0;
	            for (var i = 0; i < checkboxes.length; i++) {
                    if (checkboxes[i].checked)
                        checked++;
		            checkboxes[i].checked = true;
                    problem.push(parseInt(checkboxes[i].value));
	            }

	            counter = counter + checkboxes.length - checked;
	            span.textContent = counter;
            });

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
        MathJax.typesetPromise().then(() => {
            MathJax.typesetPromise();
          }).catch((err) => console.log(err.message));

        });
};

var filterRecreate = function (paginator,resistor,SHOWN_NUMBER) {
    let fdata = new FormData(document.getElementById('filters'));
    sendRequest('POST', createUrl(paginator.id,1,SHOWN_NUMBER), fdata)
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

	        var lastDivs = document.querySelector('.counter');
            lastDivs.innerHTML = "";
            var checkboxes = document.querySelectorAll('.checkbox-check');

            var check = function (checkbox) {
                checkbox.onclick = function() {
		            if (checkbox.checked) {
			            counter++;
                        problem.push(parseInt(checkbox.value));
		            } else {
			            counter--;
                        problem = problem.filter(function(value, index, arr) {
                            return value !== parseInt(checkbox.value);
                        });
		            }
		            span.textContent = counter;
	            };
            };

            var divs = document.querySelector('.counter');
            var clear = document.createElement('button');
            var span = document.createElement('span');
            var selectAll = document.createElement('button');
            selectAll.textContent = "Выбрать всё";
            clear.textContent = "Очистить";

            for (var i = 0; i < checkboxes.length; i++) {
                if (problem.includes(parseInt(checkboxes[i].value)))
                    checkboxes[i].checked = true;
	            check(checkboxes[i]);
            }

            divs.appendChild(span);
            divs.appendChild(clear);
            divs.appendChild(selectAll);
            span.textContent = counter;

            clear.onclick = function(evt) {
	            evt.preventDefault();

	            for (var i = 0; i < checkboxes.length; i++) {
		            checkboxes[i].checked = false;
	            }

                problem = [];
	            counter = 0;
	            span.textContent = counter;
            };

            selectAll.addEventListener('click' , function(evt) {
	            evt.preventDefault();

                let checked = 0;
	            for (var i = 0; i < checkboxes.length; i++) {
                    if (checkboxes[i].checked)
                        checked++;
		            checkboxes[i].checked = true;
                    problem.push(parseInt(checkboxes[i].value));
	            }

	            counter = counter + checkboxes.length - checked;
	            span.textContent = counter;
            });

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
            MathJax.typesetPromise().then(() => {
                MathJax.typesetPromise();
            }).catch((err) => console.log(err.message));
      });
};

var createPaginator = async function (paginator,SHOWN_NUMBER,amount) {
        let fdata = new FormData(document.getElementById('filters'));
        await sendRequest('POST', createUrl(paginator.id,1,SHOWN_NUMBER), fdata)
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
            MathJax.typesetPromise().then(() => {
                MathJax.typesetPromise();
            }).catch((err) => console.log(err.message));
        });
};

var startFunction = async function(paginators,amounts) {
    for (var i = 0; i < paginators.length; i++) {
        await createPaginator(paginators[i],SHOWN_NUMBER,amounts[i]);
    }
    var checkboxes = document.querySelectorAll('.checkbox-check');
    var studentChecks = document.querySelectorAll('.checkbox-student');


    var check = function (checkbox) {
        checkbox.onclick = function() {
		    if (checkbox.checked) {
			    counter++;
                problem.push(parseInt(checkbox.value));
		    } else {
			    counter--;
                problem = problem.filter(function(value, index, arr) {
                    return value !== parseInt(checkbox.value);
                });
		    }
		    span.textContent = counter;
	    };
    };

    var checkStudent = function (checkbox) {
        checkbox.onclick = function () {
            if (checkbox.checked)
                student.push(parseInt(checkbox.value));
            else
                student = student.filter(function (value, index, arr) {
                    return value !== parseInt(checkbox.value);
                });
        };
    };

    if (createTest !== null) {
        createTest.addEventListener('click', async function (evt) {
            evt.preventDefault();

            let fdata = new FormData();
            fdata.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
            fdata.append('submit', 'Создать тест');
            fdata.append('name', document.querySelector('#testName').value);
            fdata.append('problem', problem.join(','));
            await sendRequest('POST', '/problems/assign', fdata).then(data => location.reload());
        });
    }

    if (assignProb !== null) {
        assignProb.addEventListener('click', async function(evt) {
            evt.preventDefault();

            let fdata = new FormData();
            fdata.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
            fdata.append('submit', 'Назначить задачи');
            fdata.append('date_deadline', document.getElementsByName('date_deadline')[0].value);
            fdata.append('problem', problem.join(','));
            fdata.append('student', student.join(','));
            await sendRequest('POST', '/problems/assign', fdata).then(data => location.reload());
        });
    }


    var divs = document.querySelector('.counter');
    var clear = document.createElement('button');
    var span = document.createElement('span');
    var selectAll = document.createElement('button');
    selectAll.textContent = "Выбрать всё";
    clear.textContent = "Очистить";

    for (var i = 0; i < checkboxes.length; i++) {
	    check(checkboxes[i]);
    }
    for (var i = 0; i < studentChecks.length; i++) {
        checkStudent(studentChecks[i]);
    }

    divs.appendChild(span);
    divs.appendChild(clear);
    divs.appendChild(selectAll);
    span.textContent = "0";

    clear.onclick = function(evt) {
	    evt.preventDefault();

	    for (var i = 0; i < checkboxes.length; i++) {
		    checkboxes[i].checked = false;
	    }

        problem = [];
	    counter = 0;
	    span.textContent = counter;
    };

    selectAll.addEventListener('click' , function(evt) {
	    evt.preventDefault();

        let checked = 0;
	    for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked)
                checked++;
		    checkboxes[i].checked = true;
            problem.push(parseInt(checkboxes[i].value));
	    }

	    counter = counter + checkboxes.length - checked;
	    span.textContent = counter;
    });
};

window.onload = function () {
    startFunction(paginators,amounts);
};