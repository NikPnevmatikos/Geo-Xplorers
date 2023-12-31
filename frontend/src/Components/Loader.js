import LoadingOverlay from 'react-loading-overlay';
import { Modal } from "@mui/material";
import Spinner from 'react-bootstrap/Spinner';

export default function Loader({isActive}) {

    return(

        <Modal
            open={isActive}
            aria-labelledby="modal-title"
            aria-describedby="modal-description"
            style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
            }}
        >
            <Spinner animation="grow" role="status">
                <span className="visually-hidden">Loading...</span>
            </Spinner>
        </Modal>
    )

}