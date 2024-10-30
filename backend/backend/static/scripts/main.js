
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
            
            // Обновляем информацию в блоке info__wrapper
            infoWrapper.innerHTML = `
              <div class="info__name">${sequenceData[0].id}</div>
              <div class="info__desc">${sequenceData[0].name}</div>
            `;
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
            <div>${interpData[0].id}</div>
            <div>${interpData[0].n_value}</div>
            <div>${interpData[0].description}</div>
            <div">${interpData[0].example_text}</div>
          `;

      } else {
        console.error('Ошибка при загрузке последовательности');
      }
    } catch (error) {
      console.error('Произошла ошибка:', error);
    }
}

const selector = document.querySelector('.main__header-select');
selector.addEventListener('change', function(event) {
  loadInterpretations_details();
});