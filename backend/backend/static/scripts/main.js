document.addEventListener('DOMContentLoaded', loadSequenceList);


document.getElementById('find').addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    event.preventDefault(); 
    executeSearchQuery();
  }
});

async function loadSequenceList() {
  try {
    const response = await fetch(`/search_seq`);
    if (response.ok) {
      const sequenceData = await response.json(); 
      const infoWrapper = document.querySelector('.home__find-href'); 
      infoWrapper.innerHTML = ''; 

      // Проверяем структуру данных
      console.log('Полученные данные:', sequenceData);

      sequenceData.slice(0, 4).forEach((seq) => {
        const a = document.createElement('a');
        a.classList.add('home__find-href-content');
        a.href = `/main?find=${seq.OEIS_ID}`;
        a.textContent = seq.OEIS_ID;
        infoWrapper.appendChild(a);
    });

    } else {
      console.error('Ошибка при загрузке последовательности: ', response.status);
    }
  } catch (error) {
    console.error('Произошла ошибка:', error);
  }
}





document.addEventListener('DOMContentLoaded', function() {
    const oeisId = document.querySelector('.main__header-name').textContent.trim();
    
    async function loadInterpretations(oeisId) {
      try {
        const response = await fetch(`/search_interp?oeis_id=${oeisId}`);
        if (response.ok) {
          const interpretations = await response.json();
          const selector = document.querySelector('.main__header-select');
          selector.innerHTML = ''; // Очищаем текущие опции

          const addedDescriptions = new Set(); // Создаём Set для отслеживания уникальных interp.desc
  
              interpretations.forEach((interp) => {
                  if (!addedDescriptions.has(interp.desc)) {
                      const option = document.createElement('option');
                      option.textContent = interp.interpretation_name; // Название интерпретации
                      option.value = interp.endpoint;   // Устанавливаем эндпоинт как значение
                      selector.appendChild(option);
  
                      // Добавляем interp.desc в Set, чтобы отслеживать добавленные элементы
                      addedDescriptions.add(interp.interpretation_name);
                  }
              });

        loadInterpretations_details();
        } else {
          console.error('Ошибка при загрузке интерпретаций');
        }
      } catch (error) {
        console.error('Произошла ошибка:', error);
      }
    }

    async function loadSequence(oeisId) {
        try {
          const response = await fetch(`/search?oeis_id=${oeisId}`);
          if (response.ok) {
            const sequenceData = await response.json();
            const infoWrapper = document.querySelector('.info__block1');
            infoWrapper.innerHTML = `
                  <div class="info__block1">${sequenceData[0].sequence_description}</div>
            `; 

          MathJax.typesetPromise([infoWrapper]).catch((err) => console.log(err.message));

          } else {
            console.error('Ошибка при загрузке последовательности');
          }
        } catch (error) {
          console.error('Произошла ошибка:', error);
        }
    }

    if (oeisId) {
      loadInterpretations(oeisId);
      loadSequence(oeisId);
      loadAlgorithmsByInterpretation();
    }
});


async function loadInterpretations_details() {
    const selector = document.querySelector('.main__header-select');
    const interpretation_name = selector.options[selector.selectedIndex].text;

    try {
      const response = await fetch(`/interp?interpretation_name=${interpretation_name}`);
      if (response.ok) {
        const interpData = await response.json();
        const infoWrapper = document.querySelector('.info__block2');
            infoWrapper.innerHTML = `
            <div>${interpData[0].example_text}</div>
          `;
      } else {
        console.error('Ошибка при загрузке последовательности');
      }

      loadAlgorithmsByInterpretation();
     
    } catch (error) {
      console.error('Произошла ошибка:', error);
    }
}

const selector = document.querySelector('.main__header-select');
selector.addEventListener('change', function(event) {
  loadInterpretations_details();
});

async function loadAlgorithmsByInterpretation(Interp_ID) {
  try {
    const Interp_ID = document.querySelector('.for_interp_id').textContent.trim();
    const response = await fetch(`/alg?interp_id=${Interp_ID}`);
    if (response.ok) {
      const algorithms = await response.json();
      const selector_alg = document.querySelector('.func-block__left-select');
      selector_alg.innerHTML = ''; // Очищаем текущие опции
      
      algorithms.forEach((alg) => {
        const option = document.createElement('option');
        option.textContent = alg.alg_name; // Название алгоритма
        option.value = alg.Alg_ID; // ID алгоритма
        selector_alg.appendChild(option);
      });
      loadAlgorithm_details()
    } else {
      console.error('Ошибка при загрузке алгоритмов');
    }
  } catch (error) {
    console.error('Произошла ошибка:', error);
  }
}


const selectorAlg = document.querySelector('.func-block__left-select');

async function loadAlgorithm_details() {
  
  const algName = selectorAlg.options[selectorAlg.selectedIndex].text;

  try {
    const response = await fetch(`algDetails?algName=${algName}`);
    if (response.ok) {
      const algData = await response.json();
      
      const infoWrapper = document.querySelector('.func-block__right'); // Находим основной контейнер
      infoWrapper.innerHTML = ''; 

      infoWrapper.innerHTML = `
       <div class="func-block__right">
        <div class="func-block__right-name">${algData[0].field_name}</div>
        <div class="func-block__right-desc">${algData[0].field_description}</div>
      </div>
    `;
    const infoWrapper2 = document.querySelector('.func-block__left-param'); // Контейнер для параметров
const infoWrapper3 = document.querySelector('.func-block__left-functional'); // Функциональный контейнер

// Очищаем контейнеры
infoWrapper2.innerHTML = '';
infoWrapper3.innerHTML = '';


// Разбиваем параметры на отдельные элементы
const titles = algData[0].parameters_name.split(',');
const algType = algData[0].alg_type;
console.log(algType);
// Генерация элементов
titles.forEach((title) => {
  const titleTrimmed = title.trim();

  
  // Создаем div для параметра
  const titleDiv = document.createElement('div');
  titleDiv.textContent = titleTrimmed + "=";

  const input = document.createElement('input');
  input.type = 'number';
  input.classList.add('func-block__left-param-input');

  titleDiv.appendChild(input);
  infoWrapper2.appendChild(titleDiv); // Добавляем в контейнер параметров
  
});
if(algType == 'Rank'){
    // Создаем объект для "Комбинаторного объекта"
    const objectDiv = document.createElement('div');
    objectDiv.classList.add('func-block__left-object');
    objectDiv.textContent = 'Комбинаторный объект';
  
    infoWrapper3.appendChild(objectDiv); // Добавляем в функциональный блок
  
    const objectInput = document.createElement('input');
    objectInput.type = 'text';
    objectInput.classList.add('func-block__left-param-input1', 'func-block__left-param-input--wd500');
  
    infoWrapper3.appendChild(objectInput); // Добавляем input для объекта
}
else if(algType == 'Unrank'){
    // Создаем объект для "Комбинаторного объекта"
    const objectDiv = document.createElement('div');
    objectDiv.classList.add('func-block__left-object');
    objectDiv.textContent = 'Ранг';
  
    infoWrapper3.appendChild(objectDiv); // Добавляем в функциональный блок
  
    const objectInput = document.createElement('input');
    objectInput.type = 'number';
    objectInput.classList.add('func-block__left-param-input2');
  
    infoWrapper3.appendChild(objectInput); // Добавляем input для объекта
}
// Вставляем infoWrapper2 в infoWrapper3 перед блоком "Комбинаторный объект"
infoWrapper3.insertBefore(infoWrapper2, infoWrapper3.querySelector('.func-block__left-object'));
   
    } else {
      console.error('Ошибка при загрузке последовательности');
    }
   
  } catch (error) {
    console.error('Произошла ошибка:', error);
  }
}

selectorAlg.addEventListener('change', function(event) {
  loadAlgorithm_details();
  const textArea = document.querySelector('.func-block__left-main_textarea');
  textArea.innerHTML = '';
});

async function solve() {
  const textArea = document.querySelector('.func-block__left-main_textarea');
  textArea.innerHTML = '';
  const inputs = document.querySelectorAll(".func-block__left-param-input"); // Находим все динамические input
  const inputCombObject = document.querySelectorAll(".func-block__left-param-input1");
  const inputRank = document.querySelectorAll(".func-block__left-param-input2")
  const algName = selectorAlg.options[selectorAlg.selectedIndex].text;
  const response = await fetch(`/algDetails?algName=${algName}`);
  const algData = await response.json();
  var alg_id = algData[0].Alg_ID
  const params = {};

  inputs.forEach((input, index) => {
      params[`param${index + 1}`] = input.value; // Собираем значения в объект
  });
  if(inputCombObject != null){
    inputCombObject.forEach((input,index) =>{
      params['combObject'] = input.value;
  });
  };
  if(inputRank != null){
    inputRank.forEach((input,index) =>{
      params['Rank'] = input.value;
  });
};
  console.log(params['combObject']);
  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
  console.log("Параметры",params)
  try {
      const response = await fetch('/solve', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken  // Добавляем CSRF-токен в заголовок
          },
          body: JSON.stringify({
            params: params,  // Передаем объект параметров
            alg_id: alg_id,   // Передаем идентификатор алгоритма
        }),
    });

      if (!response.ok) throw new Error("Ошибка запроса");

      const result = await response.json();
      document.getElementById("func-block__left-main_textarea").textContent = result; // Выводим результат
  } catch (error) {
      console.error("Произошла ошибка:", error);
      document.getElementById("func-block__left-main_textarea").textContent = "Ошибка вычислений";
  }
};
