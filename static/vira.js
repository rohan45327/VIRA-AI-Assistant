const micBtn = document.getElementById('micBtn');
const chatLog = document.getElementById('chat-log');
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const SpeechSynthesis = window.speechSynthesis;
const active = new Audio('static/assets/wake.mp3');
const errorSound = new Audio('static/assets/sleep.mp3');
const dice = new Audio('static/assets/dice.mp3');
const laugh = new Audio('static/assets/laugh.mp3');
const coin = new Audio('static/assets/coin.mp3');
const inpu = document.getElementById('keyboard');
const keybut = document.getElementById('but');
const fileinput = document.getElementById('file-input');
const msg=document.getElementById('msg');
const instr=document.getElementById('instr');
const tim=document.getElementById('time');
function updatecl(){
    let now=new Date();
    let hrs=now.getHours();
    let mins=now.getMinutes();
    let sec=now.getSeconds();
    hrs=hrs<10?'0'+hrs:hrs;
    mins=mins<10?'0'+mins:mins;
    sec=sec<10?'0'+sec:sec;
    const str=`${hrs}:${mins}:${sec}`;
    tim.textContent=str;
}
setInterval(updatecl,1000);
let recognition;
let isListening = false;
let expectingSpeech = false;
let availableVoices = [];
const usrname='Chandu';
const upbut=document.getElementById('uploadBtn')
const filen=document.getElementById('filein')
speechSynthesis.onvoiceschanged = () => {
    availableVoices = speechSynthesis.getVoices();
};
function plays(audio) {
    audio.pause();
    audio.currentTime = 0;
    audio.play().catch(e => console.error("Error playing sound:", e));
}
let arr=["Vira: How can I help you?",
         "Vira: How can I assist you Today?",
         "Vira: Ready to go.",
         "Vira: What's on your Mind?",
         "Vira: How's your Day?"
]
let idx=Math.floor(Math.random()*arr.length);
msg.textContent=`${arr[idx]}`;
upbut.addEventListener('click',()=>{
    filen.click();
})
filen.addEventListener('change',(e)=>{
    const filo = e.target.files[0];
    let ins = inpu.value.trim(); 
    if(!ins){
        ins='Analyze and review this file.'
    }
    if(!filo){
        addMessage('Vira', 'Error please select an file to open')
    }
    else{
        sendFileToVira(ins,filo)
        inpu.value=''
    }
})
function msgskull(){
    const ads=document.createElement('div')
    ads.classList.add('message','jarvis-message','skull')
    ads.id='vira-skull';
    chatLog.appendChild(ads);
    chatLog.scrollTop=chatLog.scrollHeight;
    return ads;
}
function addMessage(sender, text){
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'jarvis-message');
    messageDiv.textContent = (sender === 'user' ? `${usrname}: ` : 'Vira: ');
    chatLog.appendChild(messageDiv);
    let ind=0;
    if(sender==='Vira'){
        const type=setInterval(()=>{
        if(ind<=text.length && text.length<200){
            messageDiv.textContent+=text.charAt(ind);
            ind++;
        }
        else{
            clearInterval(type);
            let formated=text.replace("/ /", '').replace(/\*\*(.*?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>').replace(/```[\s\S]*?```/g, match => `<pre>${match.slice(3,-3)}</pre>`).replace(/`([^`]*)`/g, '<code>$1</code>');
            messageDiv.innerHTML='Vira: '+formated;
            const copybtn=document.createElement('button');
            copybtn.className='copy-but'; 
            copybtn.textContent='\u29C9';
            copybtn.title='Copy to Clipboard';
            copybtn.addEventListener('click',(event)=>{
                event.stopPropagation();
                navigator.clipboard.writeText(text)
                .then(()=>{
                    copybtn.textContent = '✔';
                    setTimeout(()=> {
                        copybtn.textContent='\u29C9';
                    }, 1000);
                })
            })
            messageDiv.appendChild(copybtn);
        }
    },10);
    scroll();
    }
    else{
        messageDiv.textContent = (sender === 'user' ? `${usrname}: ` : 'Vira: ') + text;
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight;
    }
}
function scroll(){
    chatLog.scrollTop=chatLog.scrollHeight;
}
function speak(text, rates = 1.0, pitchs = 0.78, onEndCallback = null) {
    if (SpeechSynthesis) {
        const utterance = new SpeechSynthesisUtterance(text);
        const googleVoice = availableVoices.find(v => v.name.includes("Google US English Male"));
        const googleUK = availableVoices.find(v => v.name.includes("Google UK English Male"));
        const msMark = availableVoices.find(v => v.name === "Microsoft Mark - English (United States) en-US");
        const msZira = availableVoices.find(v => v.name === "Microsoft Zira - English (United States) en-US");
        if (googleVoice) {
            utterance.voice = googleVoice;
            utterance.lang = googleVoice.lang;
        } else if (googleUK) {
            utterance.voice = googleUK;
            utterance.lang = googleUK.lang;
        } else if (msMark) {
            utterance.voice = msMark;
            utterance.lang = msMark.lang;
        } else if (msZira) {
            utterance.voice = msZira;
            utterance.lang = msZira.lang;
        }
        utterance.rate = rates;
        utterance.pitch = pitchs;
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
        };
        
        if (onEndCallback && typeof onEndCallback === 'function') {
            utterance.onend = onEndCallback;
        }

        if (speechSynthesis.speaking) {
            speechSynthesis.cancel();
        }

        speechSynthesis.speak(utterance);
    } else {
        console.warn('Web Speech Synthesis API not supported. Vira cannot speak.');
    }
}
async function sendCommandToVira(command) {
    const loader=msgskull();
    try{
        const response = await fetch(`https://vira.up.railway.app/command`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: command }),
        });
        loader.remove();
        const data = await response.json();
        const jxt = data.response;
        const playUrl = data.play_url;
        console.log('Vira responded:', jxt);
        addMessage('Vira', jxt);

        if (playUrl) {
            window.open(playUrl, '_blank');
        }

        const low = jxt.toLowerCase();
        let Rate = 1.0;
        let Pitch = 0.80;
        
        if (low.includes("it is")) {
            speak(jxt, Rate, Pitch, () => dice.play());
        } else if (low.includes("joke") || low.includes("laugh")) {
            speak(jxt, Rate, Pitch, () => plays(laugh));
        } else if (low.includes("it was")) {
            speak(jxt, Rate, Pitch, () => plays(coin));
        } else {
            speak(jxt, Rate, Pitch);
        }

    } catch (error) {
        loader.remove();
        console.error('Error sending command to Vira backend:', error);
        addMessage('Vira', 'Sorry, I am having trouble connecting to my backend. Please check if the Vira server is running.');
        speak('Sorry, I am having trouble connecting to my backend. Please check if the Vira server is running.', 1, 0.9);
    }
}
async function sendFileToVira(cmd,file) {
    const loader=msgskull();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('prompt', cmd); 
    addMessage('user', `${cmd} Uploading file: ${file.name}`);
    try {
        const response = await fetch('https://vira.up.railway.app/upload', {
            method: 'POST',
            body: formData
        });
        loader.remove()
        const data = await response.json();
        const jxt = data.response;
        addMessage('Vira', jxt);
        if(instr.style.display=='block'){
            instr.style.display='none'
        }
        speak(jxt);
    } catch (error) {
        console.error('Error sending file to Vira backend:', error);
        addMessage('Vira', 'Sorry, I had trouble processing that file.');
        speak('Sorry, I had trouble processing that file.');
    }
}

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-IN';

    recognition.onstart = () => {
        isListening = true;
        expectingSpeech = true;
        plays(active);
        statusText.textContent = 'Listening... Speak now.';
        micBtn.textContent=''
        micBtn.classList.add('dots')
        micBtn.classList.add('listening');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('You said:', transcript);
        addMessage('user', transcript);
        plays(active);
        statusText.textContent = 'Processing command...';
        micBtn.classList.remove('listening');
        micBtn.classList.remove('dots')
        micBtn.textContent="🎙"
        isListening = false;
        expectingSpeech = false;
        sendCommandToVira(transcript);
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        statusText.textContent = `Error: ${event.error}. Click button to retry.`;
        micBtn.classList.remove('dots')
        micBtn.classList.remove('listening');
        micBtn.textContent="🎙"
        isListening = false;
        expectingSpeech = false;
        plays(errorSound);
        speak("I'm sorry, I couldn't understand that. Please try again.");
    };

    recognition.onend = () => {
        if (expectingSpeech) {
            plays(errorSound);
            statusText.textContent = 'I can’t hear anything. Click the mic to speak.';
            micBtn.classList.remove('dots')
            micBtn.classList.remove('listening');
            micBtn.textContent="🎙"
        }
        isListening = false;
        expectingSpeech = false;
    };

    micBtn.addEventListener('click', () => {
        if (isListening) {
            recognition.stop();
            isListening = false;
            expectingSpeech = false;
        } else {
            recognition.start();
        }
        if (speechSynthesis.speaking) {
            statusText.textContent = 'You stopped the response. Click mic button to generate another response.';
            speechSynthesis.cancel();
            isListening = false;
        }
    });

} else {
    micBtn.style.display = 'none';
    statusText.textContent = 'Speech Recognition is not supported in this browser.';
    console.error('Web Speech API not supported.');
}
document.addEventListener('keypress',(event)=>{
    if(event.key=='Enter'){
        event.preventDefault()
        const prom = inpu.value.trim();
        if(prom){
            addMessage('user', prom);
            console.log(`User : ${prom}`)
            sendCommandToVira(prom);
            inpu.value = '';
        }
        else{
            console.error("Vira: Can't recieve any prompt.")
        }
    }
})
keybut.addEventListener('click', () => {
    const prom = inpu.value.trim();
    if (prom) {
        addMessage('user', prom);
        console.log(`User : ${prom}`)
        sendCommandToVira(prom);
        inpu.value = '';
    }
    else{
        console.error("Vira: Can't recieve any prompt.")
    }

});
