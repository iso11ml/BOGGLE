var turn = 1;
var turns = 0;
var isGameStarted = false;
var interval = null;
var totalScore = 0;
var maxScore = 0;
var maxWord = 'Ninguna';
window.onload = function() {
    var playerTurnElement = document.getElementById("playerTurn");
    var minutesElement = document.getElementById("minutes");
    var secondsElement = document.getElementById("seconds");
    var playButton = document.getElementById("play-button");
    var audio = document.getElementById("myAudio");
    var openRulesButton = document.getElementById("open-rules");
    var closeButton = document.getElementById("close");
    var modalContainer = document.getElementById("ventanaEmergente");
    var playerContainer = document.querySelector('.playerContainer');

    openRulesButton.addEventListener('click', function() {
        modalContainer.classList.add("show");
    });
    closeButton.addEventListener('click', function() {
        modalContainer.classList.remove("show");
    });

    playButton.addEventListener('click', function() {
        if (!isGameStarted && turns < 2) {
            playerTurnElement.textContent = "Turno Del Jugador: " + turn;
            playerContainer.classList.remove('turn2', 'gameover'); 
            if(turn === 1) playerContainer.classList.add('turn1');
            if(turn === 2) playerContainer.classList.add('turn2');
            document.getElementById('totalScore').textContent = 'Total Score: ' + totalScore;
            document.getElementById('maxScoreWord').textContent = 'Palabra: '+ maxWord + ' Puntos: ' + maxScore;
            startTimer();
            isGameStarted = true;
            audio.play();
        } else if (turns === 2) {
            location.reload(); 
            playerContainer.classList.remove('turn1', 'turn2'); 
            playerContainer.classList.add('gameover'); 
        }
    });

    function startTimer() {
        var minutes = 0;
        var seconds = 10;
        var clockContainer = document.querySelector('.clockContainer');
        if(interval) clearInterval(interval);
        interval = setInterval(function() {
            seconds--;
            if (seconds < 0) {
                seconds = 59;
                minutes--;
            }
    
            minutesElement.textContent = minutes;
            secondsElement.textContent = seconds < 10 ? "0" + seconds : seconds;
    
            // Comprueba si quedan 10 segundos o menos y aplica la clase de parpadeo
            if (minutes === 0 && seconds <= 10) {
                clockContainer.classList.add('blink');
            } else {
                clockContainer.classList.remove('blink');
            }
    
            if (minutes === 0 && seconds === 0) {
                clearInterval(interval);
                totalScore = 0;
                maxScore = 0;
                maxWord = 'Ninguna';
                document.getElementById('maxScoreWord').textContent = 'No Hay Palabra Con La Puntuación Más Alta';
                document.getElementById('totalScore').textContent = 'Total Score: ' + totalScore;
                turn = turn === 1 ? 2 : 1;
                turns++;
                if (turns < 2) {
                    playerTurnElement.textContent = "Turno Del Jugador: " + turn;
                    playerContainer.classList.remove('turn1', 'turn2', 'gameover');
                    if(turn === 1) playerContainer.classList.add('turn1');
                    if(turn === 2) playerContainer.classList.add('turn2');
                } else {
                    playerTurnElement.textContent = "Game Over";
                    playButton.textContent = "New Game";
                    playerContainer.classList.remove('turn1', 'turn2');
                    playerContainer.classList.add('gameover');
                }
                clockContainer.classList.remove('blink');
                isGameStarted = false;
            }
        }, 1000);
    }
    const botones = document.querySelectorAll('.boggle-board button');
    let letrasSeleccionadas = '';
    let seleccionando = false;
    botones.forEach(boton => {
        boton.addEventListener('mousedown', () => {
            if (isGameStarted) {
                letrasSeleccionadas += boton.innerText;
                seleccionando = true;
                boton.classList.add('seleccionado');
                console.log(letrasSeleccionadas);
            }
        });

        boton.addEventListener('mouseenter', () => {
            if (seleccionando && isGameStarted) {
                boton.classList.add('seleccionado');
                letrasSeleccionadas += boton.innerText;
                console.log(letrasSeleccionadas);
            }
        });

        
       

        boton.addEventListener('mouseup', () => {
            if (isGameStarted) {
                seleccionando = false;
                botones.forEach(boton => {});
                if (letrasSeleccionadas !== '') {
                    fetch('/verificar-existencia/' + letrasSeleccionadas)
                    .then(response => response.json())
                    .then(data => {
                        if (data.flag) {
                            console.log(data.flag);
                            console.log(data.score);
                            console.log(data.word);
                            console
                        
                            console.log('totalScore antes de agregar: ', totalScore);
                            totalScore += data.score;
                            console.log('totalScore después de agregar: ', totalScore);
                            console.log('data.score: ', data.score);
                            botones.forEach(boton => {
                                if (boton.classList.contains('seleccionado')) {
                                    boton.classList.add('correcto');
                                    setTimeout(() => {
                                        boton.classList.remove('correcto');
                                    }, 500);
                                }
                                boton.classList.remove('seleccionado');
                            });
                            
                            let [maxWordFromServer, maxScoreFromServer] = data.max_score;
                            function capitalizarPrimeraLetra(maxWord) {
                                return maxWord.charAt(0).toUpperCase() + maxWord.slice(1);
                            }

                            if (maxScoreFromServer > maxScore) {
                                maxScore = maxScoreFromServer;
                                maxWord =  capitalizarPrimeraLetra(maxWordFromServer);
                                
                            }

                            document.getElementById('totalScore').textContent = 'Total Score: ' + totalScore;
                            document.getElementById('maxScoreWord').textContent = 'Palabra: '+ maxWord + ' Puntos: ' + maxScore;
                            const tabla = document.querySelector('.score tbody');
                            const fila = document.createElement('tr');

                            // Columna "Palabra"
                            const celdaPalabra = document.createElement('td');
                            celdaPalabra.textContent = data.word;
                            fila.appendChild(celdaPalabra);

                            // Columna "Jugador"
                            const celdaJugador = document.createElement('td');
                            celdaJugador.textContent = 'Jugador ' + turn;
                            fila.appendChild(celdaJugador);

                            // Columna "Puntuación"
                            const celdaPuntuacion = document.createElement('td');
                            celdaPuntuacion.textContent = data.score;
                            fila.appendChild(celdaPuntuacion);

                            tabla.appendChild(fila);
                        } else {
                            console.log(data.flag);
                            botones.forEach(boton => {
                                if (boton.classList.contains('seleccionado')) {
                                    boton.classList.add('incorrecto');
                                    setTimeout(() => {
                                        boton.classList.remove('incorrecto');
                                    }, 1000);
                                }
                                boton.classList.remove('seleccionado');
                            });
                        }
                    })
                    .catch(error => {
                        console.error(error);
                    })
                    .finally(() => {
                        letrasSeleccionadas = '';
                    });
                }
            }
        });
    });
};
