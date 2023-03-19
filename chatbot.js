
class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox_button'),
            chatBox: document.querySelector('.chatbox_support'),
            sendButton: document.querySelector('.send_button'),
        };

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;
        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        }) 
    }

    toggleState(chatBox) {
        this.state = !this.state;
        // show or hides the box
        if (this.state) {
            chatBox.classList.add('chatbox--active');
        } else {
            chatBox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatBox) {
        var textField = chatBox.querySelector('input');
        let text1 = textField.value;
        if (text1 === "") {
            return;
        }
        let msg1 = {name: "User", message: text1};
        this.messages.push(msg1);

        fetch($SCRIPT_ROOT).then(r =>  r.json()).then(resp => {
            let msg2 = {name: "Travis", message: resp.answer};
            this.messages.push(msg2);
            this.updateChatText();
            textField.value = '';
        }).catch((error) => {
            console.log(error);
            this.updateChatText();
            textField.value = '';
        });
    }
    updateChatText() {
        // var html = '';

        let my_dict = {
            "Hi" : "Hey",
            "What is your name?": "My name is Travis",
            "How are you?" : "I am fine",
            "What are the tourist places near me?" : "Where do you live?",
            "Top 10 places in Delhi" : "1. Humayun's Tomb <br>2. Jama Masjid <br>3. Lotus Temple <br>4. Rashtrapati Bhavan <br>5. Clubbing in Hauz Khaus Village <br>6. Jantar Mantar <br>7. Partying at the Connaught Palace <br>8. Shop at Chandni Chowk <br>9. Morning walk near India Gate <br>10. Tour the National Zoological Park"
        }

        // "Places in Delhi" : 
            // "Places to visit in Delhi" : ,
            // "Trending places in Delhi" : 
            // "Things to do in Delhi" :
            // ""    

        var response, conversation, input;
        response = "Something went wrong!";
        conversation = document.getElementById("chatbot-conversation");
        input = document.getElementById("chatbot-input").value;
        for (let k in my_dict)
        {
            if (input == k) {
                conversation.innerHTML += '<div class="messages_item messages_item--operator">' + my_dict[k] + '</div>'
                conversation.innerHTML += '<div class="messages_item messages_item--visitor">' + input + '</div>'
            }
        }
        // this.messages.slice().reverse().forEach(function(item) {
        // if (item.name === "Travis")
        // {
        //     html += '<div class="messages_item messages_item--visitor">' + response + '</div>'
        // } 
        // else 
        // {
        //     html += '<div class="messages_item messages_item--operator">' + text1 + '</div>'
        // }  
        // });
        
        // const chatmessage = chatBox.querySelector('.chatbox_messages');
        // chatmessage.innerHTML = html;
    }
}

const chatBox = new Chatbox();
chatBox.display();