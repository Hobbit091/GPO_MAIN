
function switchLanguage(language) {
    document.getElementById('ru').classList.remove('active');
    document.getElementById('en').classList.remove('active');
    document.getElementById(language).classList.add('active');
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

          interpretations.forEach((interp) => {
            const option = document.createElement('option');
            option.textContent = interp.desc; // Название интерпретации
            option.value = interp.endpoint;   // Устанавливаем эндпоинт как значение
            selector.appendChild(option);
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
                  <h4 style="text-decoration:underline"> Начальные значения </h4>
                  <div>${sequenceData[0].recurrent_formula}</div>
                  <div>Значения a(n) так известны как ${sequenceData[0].name}</div>
                  <div>Значения a(n) зависят от ${sequenceData[0].number_of_parameters} параметров</div>
                  <h4 style="text-decoration:underline"> Основные формулы </h4>
                  <div style="padding-left:10px"> Явная формула </div>
                  <div class="main_info_formula"> $$${sequenceData[0].explicit_formula_latex}$$</div>
                   <div style="padding-left:10px"> Рекуррентная формула: </div>
                  <div class="main_info_formula">$$${sequenceData[0].recurrent_formula_latex}$$</div>
                   <div style="padding-left:10px"> Другая формула </div>
                  <div class="main_info_formula">$$${sequenceData[0].other_formula_latex}$$</div>
                   <div style="padding-left:10px"> Производящая функция</div>
                  <div class="main_info_formula">$$${sequenceData[0].generating_function_latex}$$</div>
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
    }
});


async function loadInterpretations_details() {
    const selector = document.querySelector('.main__header-select');
    const interpDesc = selector.options[selector.selectedIndex].text;

    try {
      const response = await fetch(`/interp?description=${interpDesc}`);
      if (response.ok) {
        const interpData = await response.json();
        const infoWrapper = document.querySelector('.info__block2');
            infoWrapper.innerHTML = `
            <div> Значения a(n) определяет количество ${interpData[0].n_value} элементов</div>
            <div> Определение интерпретации: ${interpData[0].description} </div>
            <div> Пример: </div>
            <div style="display:none" class="for_interp_id">${interpData[0].id}</div>
            <div>${interpData[0].example_text}</div>
            <div>${interpData[0].example_table}</div>
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
        option.textContent = alg.name; // Название алгоритма
        option.value = alg.id; // ID алгоритма
        selector_alg.appendChild(option);
      });
    } else {
      console.error('Ошибка при загрузке алгоритмов');
    }
  } catch (error) {
    console.error('Произошла ошибка:', error);
  }
}

