package org.enspy.4gi.domain.exceptions.already_exists;


public class EntityAlreadyExistsException extends RuntimeException {
    public EntityAlreadyExistsException(String message) {
        super(message);
    }
}