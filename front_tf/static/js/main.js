$(function() {
    var INDEX = 0; 
    $("#chat-submit").click(function(e) {
      e.preventDefault();
      var msg = $("#chat-input").val(); 
      if(msg.trim() == ''){
        return false;
      }
      generate_message(msg, 'self');
      var buttons = [
          {
            name: 'Existing User',
            value: 'existing'
          },
          {
            name: 'New User',
            value: 'new'
          }
        ];
        function messageBot(msg){
          fetch('http://127.0.0.1:5000/'+ msg)
          .then(function (response) {
              return response.json();
          }).then(data => {
              // console.log(Object.values(data)[0]["reponse"]);
              return Object.values(data)[0]["reponse"];
         });
      };
      async function test(msg){

        
        let url = ('http://127.0.0.1:5000/'+ msg);
        let response = await fetch(url);
        
        let commits = await response.json(); // read response body and parse as JSON
        // console.log(commits.reponse.reponse)
        var bot = commits.reponse.reponse
        if (msg === "Bonjour"){
          bot = "Bonjour, je suis l'assistant de Simplon, je suppose que vous avez des questions.</br>";
        }
        setTimeout(function(){
          generate_message(bot,'user');
        },100)
      }
      test(msg)

    })

    //   test(msg);
    //   if (msg === "Bonjour"){
    //     bot = "Bonjour, je suis l'assistant de Simplon, je suppose que vous avez des questions.</br>";
    //     //bot+= "<br>";
    //     //bot+= "Vous souhaitez être :</br>";
    //     //bot+= "<br>";
    //     //bot+= "<button class='bienvenue' onclick='chatbot.getReply('Apprenant')'>Apprenant</button>";
    //     //bot+= "<button class='bienvenue' onclick='chatbot.getReply('Partenaire')'>Partenaire</button>";
    //   }
    //   setTimeout(function() {      
    //     generate_message(bot, 'user');  
    //   }, 1000)
      
    // })
    
    function generate_message(msg, type) {
      INDEX++;
      var str="<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\"><span class=\"msg-avatar\"><img src=\"static/"+type+".png\"><\/span><div class=\"cm-msg-text\">"+msg+"<\/div><\/div>";
      $(".chat-logs").append(str);
      $("#cm-msg-"+INDEX).hide().fadeIn(300);
      if(type == 'self'){
       $("#chat-input").val(''); 
      }    
      $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);    
    }  
    
    $(document).delegate(".chat-btn", "click", function() {
      var value = $(this).attr("chat-value");
      var name = $(this).html();
      $("#chat-input").attr("disabled", false);
      generate_message(name, 'self');
    })
    
    $("#chat-circle").click(function() {    
      $("#chat-circle").toggle('scale');
      $(".chat-box").toggle('scale');
    })
    
    $(".chat-box-toggle").click(function() {
      $("#chat-circle").toggle('scale');
      $(".chat-box").toggle('scale');
    })
    
  })