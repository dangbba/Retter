import { useState } from "react";
import { connect } from "react-redux";
import { setMessage } from "../../store/actions/cardActions";
import { useNavigate } from "react-router-dom";
import { sendMessage } from "../../api/message";

function mapDispatchToProps(dispatch) {
  return {
    setMessage: (message) => dispatch(setMessage(message)),
  };
}

export default connect(null, mapDispatchToProps)(Message);

function Message({ setMessage }) {
  const [text, setText] = useState("");
  const voices = [1, 2, 3, 4, 5, 6];
  const [isVoiceVisible, setIsVoiceVisible] = useState(false);
  const [voice, setVoice] = useState(1);
  const navigate = useNavigate();
  const handleChange = ({ target: { value } }) => {
    setText(value);
  };

  const checkMessage = () => {
    if (text === "") {
      alert("메세지를 입력해주세요!");
      return;
    }

    // 1. 영어 삭제
    // 아래 전처리된 문장이 서버로 보내지고, 사용자에게는 이 텍스트로만 보임
    const nextText = text.replace(/\w/g, "");
    setMessage(nextText);

    // 2. 서버로 전송할 메세지 전처리
    let preprocessedText = nextText.replace(
      /[^ㄱ-ㅎ|ㅏ-ㅣ|가-힣|0-9|.?! ]/g,
      ""
    );
    // 온점, 느낌표, 물음표 1개만 남김
    preprocessedText = preprocessedText.replace(/\.+/g, ".");
    preprocessedText = preprocessedText.replace(/!+/g, "!");
    preprocessedText = preprocessedText.replace(/\?+/g, "?");

    const params = {
      id: voice,
      message: preprocessedText,
    };
    sendMessage(
      params,
      (response) => console.log(response),
      (error) => console.log(error)
    );
    // todo: 서버로 메세지 보내는 로직
    navigate("/card/edit");
  };

  return (
    <main>
      메세지 입력
      <textarea
        value={text}
        maxLength="100"
        onChange={handleChange}
        placeholder="메세지를 입력해주세요!"
      ></textarea>
      <ul>
        <li>
          Re:tter는 한글, 숫자만 지원해요. (메세지에 영어가 들어가면 자동으로
          삭제됩니다.)
        </li>
        <li>{voice}번째 음성 선택 중</li>
      </ul>
      <nav>
        <button onClick={() => setIsVoiceVisible(true)}>음성 선택</button>
        <button onClick={checkMessage}>카드 만들기</button>
      </nav>
      {isVoiceVisible ? (
        <section>
          <ul>
            {voices.map((voice) => (
              <li key={voice} onClick={() => setVoice(voice)}>
                음성 {voice}
              </li>
            ))}
          </ul>
          <button onClick={() => setIsVoiceVisible(false)}>닫기</button>
        </section>
      ) : null}
    </main>
  );
}